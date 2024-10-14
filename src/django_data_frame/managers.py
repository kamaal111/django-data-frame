from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Generic, TypeVar

import narwhals as nw
import polars as pl
from django.db import connection, models


class DataFrameQuerySet(models.QuerySet):
    def to_polars(self) -> pl.LazyFrame:
        return self.to_eager_polars().lazy()

    def to_eager_polars(self) -> pl.DataFrame:
        return pl.read_database(
            query=self.__parse_sql_statement(),
            connection=connection,
        )

    def to_narwhals_from_polars(self) -> nw.LazyFrame[pl.LazyFrame]:
        nw_data_frame = nw.from_native(self.to_polars())
        assert isinstance(nw_data_frame, nw.LazyFrame)

        return nw_data_frame

    def to_narwhals_from_eager_polars(self) -> nw.DataFrame[pl.DataFrame]:
        nw_data_frame = nw.from_native(self.to_eager_polars())
        assert isinstance(nw_data_frame, nw.DataFrame)

        return nw_data_frame

    def __parse_sql_statement(self):
        statement, params = self.query.sql_with_params()

        def map_param(param: Any):
            if isinstance(param, str):
                return f"'{param}'"
            if isinstance(param, datetime):
                return f"'{param.isoformat()}'"

            return param

        return (statement % tuple(map(map_param, params))).__str__()


DataFrameModel = TypeVar("DataFrameModel", bound=models.Model)


class DataFrameManager(
    models.Manager.from_queryset(DataFrameQuerySet), Generic[DataFrameModel]
):
    def to_polars(self) -> pl.LazyFrame:
        return self.all().to_polars()

    def to_eager_polars(self) -> pl.DataFrame:
        return self.all().to_eager_polars()

    def to_narwhals_from_polars(self) -> nw.LazyFrame[pl.LazyFrame]:
        return self.all().to_narwhals_from_polars()

    def to_narwhals_from_eager_polars(self) -> nw.DataFrame[pl.DataFrame]:
        return self.all().to_narwhals_from_eager_polars()

    def values(
        self, *fields: str | models.Combinable, **expressions: Any
    ) -> DataFrameValuesQuerySet[DataFrameModel]:
        # Just for the sake of typing it well!
        return super().values(*fields, **expressions)  # type: ignore


# This class is there just to extend the types on `ValuesQuerySet` so should
# ony be used to assist with type hinting.
if TYPE_CHECKING:
    from django.db.models.query import ValuesQuerySet

    DataFrameValuesQuerySetModel = TypeVar(
        "DataFrameValuesQuerySetModel", bound=models.Model
    )

    class DataFrameValuesQuerySet(
        ValuesQuerySet[DataFrameValuesQuerySetModel, Dict[str, Any]]
    ):
        def to_polars(self) -> pl.LazyFrame: ...

        def to_eager_polars(self) -> pl.DataFrame: ...

        def to_narwhals_from_polars(self) -> nw.LazyFrame[pl.LazyFrame]: ...

        def to_narwhals_from_eager_polars(self) -> nw.DataFrame[pl.DataFrame]: ...
