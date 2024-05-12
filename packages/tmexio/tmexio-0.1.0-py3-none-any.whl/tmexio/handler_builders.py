from __future__ import annotations

from collections import OrderedDict, defaultdict
from collections.abc import Awaitable, Callable, Iterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from inspect import (
    Parameter,
    Signature,
    isasyncgenfunction,
    iscoroutinefunction,
    isgeneratorfunction,
    signature,
)
from typing import Annotated, Any, Generic, TypeVar, get_args, get_origin

from asgiref.sync import sync_to_async
from pydantic import BaseModel, create_model

from tmexio import markers, packagers
from tmexio.event_handlers import (
    AsyncConnectHandler,
    AsyncDisconnectHandler,
    AsyncEventHandler,
    BaseAsyncHandler,
    BaseDependency,
    ContextualDependency,
    ValueDependency,
)
from tmexio.exceptions import EventException
from tmexio.server import AsyncServer, AsyncSocket
from tmexio.specs import HandlerSpec
from tmexio.structures import ClientEvent
from tmexio.types import DependencyCacheKey


class Depends:
    def __init__(
        self,
        function: DependencyCacheKey,
        exceptions: list[EventException],
        dependencies: list[Depends],
    ) -> None:
        self.function = function
        self.exceptions = exceptions
        self.dependencies = dependencies


@dataclass()
class BuilderContext:
    marker_definitions: set[markers.Marker[Any]] = field(default_factory=set)
    body_annotations: dict[str, Any] = field(default_factory=dict)
    dependency_order: OrderedDict[DependencyCacheKey, None] = field(
        default_factory=OrderedDict
    )  # order is reversed
    dependency_definitions: dict[DependencyCacheKey, BaseDependency] = field(
        default_factory=dict
    )
    possible_exceptions: set[EventException] = field(default_factory=set)

    def build_marker_definitions(self) -> list[markers.Marker[Any]]:
        return list(self.marker_definitions)

    def build_body_model(self) -> type[BaseModel] | None:
        if not self.body_annotations:
            return None
        return create_model(
            "Model",  # TODO better naming
            **self.body_annotations,
        )

    def build_dependency_definitions(
        self,
    ) -> list[tuple[DependencyCacheKey, BaseDependency]]:
        return [
            (key, self.dependency_definitions[key])
            for key in reversed(self.dependency_order)
        ]


Key = TypeVar("Key")


class Destinations(Generic[Key]):
    def __init__(self) -> None:
        self.collection: dict[Key, set[str]] = defaultdict(set)

    def add(self, key: Key, param_name: str) -> None:
        self.collection[key].add(param_name)

    def extract(self) -> list[tuple[Key, list[str]]]:
        return [
            (key, list(param_names)) for key, param_names in self.collection.items()
        ]


class RunnableBuilder:
    type_to_marker: dict[type[Any], markers.Marker[Any]] = {
        AsyncServer: markers.AsyncServerMarker(),
        AsyncSocket: markers.AsyncSocketMarker(),
        ClientEvent: markers.ClientEventMarker(),
    }

    def __init__(
        self,
        function: Callable[..., Any],
        possible_exceptions: list[EventException],
        sub_dependencies: list[Depends],
        builder_context: BuilderContext,
    ) -> None:
        self.function = function
        self.signature: Signature = signature(function)

        self.marker_destinations: Destinations[markers.Marker[Any]] = Destinations()
        self.body_destinations: Destinations[str] = Destinations()
        self.dependency_destinations: Destinations[DependencyCacheKey] = Destinations()

        self.context = builder_context
        self.context.possible_exceptions.update(possible_exceptions)
        for depends in reversed(sub_dependencies):
            self.add_sub_dependency(depends)

    def add_marker_destination(
        self, marker: markers.Marker[Any], field_name: str
    ) -> None:
        self.context.marker_definitions.add(marker)
        self.marker_destinations.add(marker, field_name)

    def add_body_field(self, field_name: str, parameter_annotation: Any) -> None:
        if get_origin(parameter_annotation) is not Annotated:
            parameter_annotation = parameter_annotation, ...
        # TODO this should check for conflicts (on context level)
        self.context.body_annotations[field_name] = parameter_annotation
        self.body_destinations.add(field_name, field_name)

    def build_sub_dependency(self, depends: Depends) -> None:
        # TODO reuse built dependencies from building other handlers
        self.context.dependency_definitions[depends.function] = DependencyBuilder(
            function=depends.function,
            possible_exceptions=depends.exceptions,
            sub_dependencies=depends.dependencies,
            builder_context=self.context,
        ).build()

    def add_sub_dependency(self, depends: Depends) -> None:
        if depends.function in self.context.dependency_order:
            self.context.dependency_order.move_to_end(depends.function)
        else:
            self.context.dependency_order[  # noqa: WPS529  # linter bug
                depends.function
            ] = None
            self.build_sub_dependency(depends)

    def add_dependency_destination(self, depends: Depends, field_name: str) -> None:
        self.add_sub_dependency(depends)
        self.dependency_destinations.add(depends.function, field_name)

    def parse_parameter(self, parameter: Parameter) -> None:
        annotation = parameter.annotation
        if isinstance(annotation, type):
            marker = self.type_to_marker.get(annotation)
            if marker is not None:
                annotation = Annotated[annotation, marker]
        args = get_args(annotation)

        if (  # noqa: WPS337
            get_origin(annotation) is Annotated
            and len(args) == 2
            and isinstance(args[1], markers.Marker)
        ):
            self.add_marker_destination(args[1], parameter.name)
        elif (  # noqa: WPS337
            get_origin(annotation) is Annotated
            and len(args) == 2
            and isinstance(args[1], Depends)
        ):
            self.add_dependency_destination(args[1], parameter.name)
        else:
            self.add_body_field(parameter.name, parameter.annotation)

    def parse_parameters(self) -> None:
        for parameter in self.signature.parameters.values():
            self.parse_parameter(parameter)

    def build_async_callable(self) -> Callable[..., Awaitable[Any]]:
        if iscoroutinefunction(self.function):
            return self.function
        elif callable(self.function):
            return sync_to_async(self.function)
        raise TypeError("Handler is not callable")


class DependencyBuilder(RunnableBuilder):
    def build(self) -> BaseDependency:
        self.parse_parameters()

        if isasyncgenfunction(self.function):
            return ContextualDependency(
                dependency_function=asynccontextmanager(self.function),
                marker_destinations=self.marker_destinations.extract(),
                body_destinations=self.body_destinations.extract(),
                dependency_destinations=self.dependency_destinations.extract(),
            )
        elif isgeneratorfunction(self.function):
            raise NotImplementedError("Sync generators are not supported")  # TODO

        return ValueDependency(
            async_callable=self.build_async_callable(),
            marker_destinations=self.marker_destinations.extract(),
            body_destinations=self.body_destinations.extract(),
            dependency_destinations=self.dependency_destinations.extract(),
        )


HandlerType = TypeVar("HandlerType", bound=BaseAsyncHandler)


class HandlerBuilder(RunnableBuilder, Generic[HandlerType]):
    def __init__(
        self,
        function: Callable[..., Any],
        possible_exceptions: list[EventException],
        sub_dependencies: list[Depends],
    ) -> None:
        super().__init__(
            function=function,
            possible_exceptions=possible_exceptions,
            sub_dependencies=sub_dependencies,
            builder_context=BuilderContext(),
        )

    def build_handler(self) -> HandlerType:
        raise NotImplementedError

    @classmethod
    def build_exceptions(cls, handler: HandlerType) -> Iterator[EventException]:
        yield from list(handler.possible_exceptions)
        if handler.body_model is None:
            yield handler.zero_arguments_expected_error
        else:
            yield handler.one_argument_expected_error

    @classmethod
    def build_spec_from_handler(
        cls,
        handler: HandlerType,
        summary: str | None,
        description: str | None,
    ) -> HandlerSpec:
        raise NotImplementedError


class EventHandlerBuilder(HandlerBuilder[AsyncEventHandler]):
    def parse_return_annotation(self) -> packagers.CodedPackager[Any]:
        annotation = self.signature.return_annotation
        args = get_args(annotation)

        if annotation is None:
            return packagers.NoContentPackager()
        elif (  # noqa: WPS337
            get_origin(annotation) is Annotated
            and len(args) == 2
            and isinstance(args[1], packagers.CodedPackager)
        ):
            return args[1]
        return packagers.PydanticPackager(annotation)

    def build_handler(self) -> AsyncEventHandler:
        self.parse_parameters()
        ack_packager = self.parse_return_annotation()

        return AsyncEventHandler(
            async_callable=self.build_async_callable(),
            marker_definitions=self.context.build_marker_definitions(),
            marker_destinations=self.marker_destinations.extract(),
            body_model=self.context.build_body_model(),
            body_destinations=self.body_destinations.extract(),
            dependency_definitions=self.context.build_dependency_definitions(),
            dependency_destinations=self.dependency_destinations.extract(),
            possible_exceptions=self.context.possible_exceptions,
            ack_packager=ack_packager,
        )

    @classmethod
    def build_spec_from_handler(
        cls,
        handler: AsyncEventHandler,
        summary: str | None,
        description: str | None,
    ) -> HandlerSpec:
        return HandlerSpec(
            summary=summary,
            description=description,
            exceptions=list(cls.build_exceptions(handler)),
            ack_code=handler.ack_packager.code,
            ack_body_schema=handler.ack_packager.body_json_schema(),
            event_body_model=handler.body_model,
        )


class ConnectHandlerBuilder(HandlerBuilder[AsyncConnectHandler]):
    def build_handler(self) -> AsyncConnectHandler:
        self.parse_parameters()

        if self.signature.return_annotation is not None:
            raise TypeError("Connection handlers can not return anything")

        return AsyncConnectHandler(
            async_callable=self.build_async_callable(),
            marker_definitions=self.context.build_marker_definitions(),
            marker_destinations=self.marker_destinations.extract(),
            body_model=self.context.build_body_model(),
            body_destinations=self.body_destinations.extract(),
            dependency_definitions=self.context.build_dependency_definitions(),
            dependency_destinations=self.dependency_destinations.extract(),
            possible_exceptions=self.context.possible_exceptions,
        )

    @classmethod
    def build_spec_from_handler(
        cls,
        handler: AsyncConnectHandler,
        summary: str | None,
        description: str | None,
    ) -> HandlerSpec:
        return HandlerSpec(
            summary=summary,
            description=description,
            exceptions=list(cls.build_exceptions(handler)),
            ack_code=None,
            ack_body_schema=None,
            event_body_model=handler.body_model,
        )


class DisconnectHandlerBuilder(HandlerBuilder[AsyncDisconnectHandler]):
    def build_handler(self) -> AsyncDisconnectHandler:
        if self.context.possible_exceptions:
            raise TypeError("Disconnection handlers can not have possible exceptions")

        self.parse_parameters()

        if self.context.build_body_model() is not None:
            raise TypeError("Disconnection handlers can not have arguments")

        if self.signature.return_annotation is not None:
            raise TypeError("Disconnection handlers can not return anything")

        return AsyncDisconnectHandler(
            async_callable=self.build_async_callable(),
            marker_definitions=self.context.build_marker_definitions(),
            marker_destinations=self.marker_destinations.extract(),
            dependency_definitions=self.context.build_dependency_definitions(),
            dependency_destinations=self.dependency_destinations.extract(),
        )

    @classmethod
    def build_spec_from_handler(
        cls,
        handler: AsyncDisconnectHandler,
        summary: str | None,
        description: str | None,
    ) -> HandlerSpec:
        return HandlerSpec(
            summary=summary,
            description=description,
            exceptions=[],
            ack_code=None,
            ack_body_schema=None,
            event_body_model=None,
        )


EVENT_NAME_TO_HANDLER_BUILDER: dict[str, type[HandlerBuilder[Any]]] = {
    "connect": ConnectHandlerBuilder,
    "disconnect": DisconnectHandlerBuilder,
}


def pick_handler_class_by_event_name(event_name: str) -> type[HandlerBuilder[Any]]:
    return EVENT_NAME_TO_HANDLER_BUILDER.get(event_name, EventHandlerBuilder)
