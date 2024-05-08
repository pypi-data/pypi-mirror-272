"""Service object implementation for SQLAlchemy.

RepositoryService object is generic on the domain model type which
should be a SQLAlchemy model.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, overload

from advanced_alchemy.service._converters import EMPTY_FILTER, to_schema

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy import RowMapping
    from sqlalchemy.sql import ColumnElement

    from advanced_alchemy.base import ModelProtocol
    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.repository.typing import ModelT
    from advanced_alchemy.service.pagination import OffsetPagination
    from advanced_alchemy.service.typing import ModelDTOT, RowMappingT


class ResultConverter:
    """Simple mixin to help convert to a paginated response model the results set is a list."""

    @overload
    def to_schema(
        self,
        data: RowMappingT,
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
    ) -> RowMappingT: ...

    @overload
    def to_schema(
        self,
        data: Sequence[RowMappingT],
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
    ) -> OffsetPagination[RowMappingT]: ...

    @overload
    def to_schema(
        self,
        data: RowMapping,
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
        schema_type: type[ModelDTOT] | None = None,
    ) -> ModelDTOT: ...

    @overload
    def to_schema(
        self,
        data: Sequence[RowMapping],
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
        schema_type: type[ModelDTOT] | None = None,
    ) -> OffsetPagination[ModelDTOT]: ...

    @overload
    def to_schema(
        self,
        data: ModelT,
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
    ) -> ModelT: ...

    @overload
    def to_schema(
        self,
        data: Sequence[ModelT],
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
    ) -> OffsetPagination[ModelT]: ...

    @overload
    def to_schema(
        self,
        data: ModelT,
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
        schema_type: type[ModelT] = ...,
    ) -> ModelT: ...

    @overload
    def to_schema(
        self,
        data: Sequence[ModelT],
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
        schema_type: type[ModelT] = ...,
    ) -> OffsetPagination[ModelT]: ...

    @overload
    def to_schema(
        self,
        data: ModelProtocol,
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
        schema_type: type[ModelDTOT] | None = None,
    ) -> ModelDTOT: ...

    @overload
    def to_schema(
        self,
        data: Sequence[ModelT],
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
        schema_type: type[ModelDTOT] | None = None,
    ) -> OffsetPagination[ModelDTOT]: ...

    def to_schema(
        self,
        data: ModelT | Sequence[ModelT] | Sequence[RowMappingT] | RowMappingT,
        total: int | None = None,
        filters: Sequence[FilterTypes | ColumnElement[bool]] | Sequence[FilterTypes] = EMPTY_FILTER,
        schema_type: type[ModelDTOT | ModelT] | None = None,
    ) -> (
        ModelT
        | OffsetPagination[ModelT]
        | ModelDTOT
        | OffsetPagination[ModelDTOT]
        | RowMapping
        | OffsetPagination[RowMappingT]
    ):
        """Convert the object to a response schema.  When `schema_type` is None, the model is returned with no conversion.

        Args:
            data: The return from one of the service calls.
            total: the total number of rows in the data
            schema_type: Collection route filters.
            filters: Collection route filters.

        Returns:
            The list of instances retrieved from the repository.
        """
        return to_schema(data=data, total=total, filters=filters, schema_type=schema_type)
