from finter.settings import get_api_client
from finter.data import ModelData
from finter.utils.index import Indexer
from finter.api.symbol_api import SymbolApi

from abc import ABCMeta, abstractmethod
from datetime import datetime
import numpy as np
import pandas as pd


def int_to_datetime(int_datetime, resolution=None, is_end=False):
    """
    to user date without time format: use int_to_datetime(int).date()
    Args:
        int_datetime: datetime with int from
        resolution: df index frequency
    """
    str_datetime = str(int_datetime)
    str_len = len(str_datetime)

    if resolution in ["minute", "second", "microsecond"] and str_len == 8:
        if is_end:
            str_datetime = str_datetime + "235959"
        else:
            str_datetime = str_datetime + "000000"

    new_str_len = len(str_datetime)
    if new_str_len == 8:
        return datetime.strptime(str_datetime, "%Y%m%d")
    elif new_str_len == 10:
        return datetime.strptime(str_datetime, "%Y%m%d%H")
    elif new_str_len == 12:
        return datetime.strptime(str_datetime, "%Y%m%d%H%M")
    elif new_str_len == 14:
        return datetime.strptime(str_datetime, "%Y%m%d%H%M%S")
    else:
        raise ValueError


class Loader(metaclass=ABCMeta):

    @abstractmethod
    def get_df(self, start: int, end: int, *args, **kwargs) -> pd.DataFrame:
        pass

    @staticmethod
    def _slice_dataframe_by_time(cm_name: str, start: int, end: int) -> pd.DataFrame:
        df = ModelData.load(cm_name)

        resolution = df.index.resolution if hasattr(df.index, "resolution") else None
        start_dt = int_to_datetime(start, resolution=resolution)
        end_dt = int_to_datetime(end, resolution=resolution, is_end=True)
        df = df.loc[start_dt:end_dt]

        return df

    def _load_cache(
        self,
        cm_name: str,
        start: int,
        end: int,
        universe=None,
        freq=None,
        fill_nan=True,
        *args,
        **kwargs
    ):

        df = self._slice_dataframe_by_time(cm_name, start, end)

        if universe is None:
            return df.reindex(
                index=pd.date_range(
                    start=str(start),
                    end=str(end),
                    freq="d"
                )
            )

        exchange, univ, inst = universe.split("-")

        df = df.reindex(
            index=Indexer(start, end, freq).get_index(
                exchange, univ, inst
            ))

        # when universe is exist(production), make last index to Nan for preventing forward looking
        if fill_nan and not df.empty:
            df.iloc[-1] = np.nan

        if "code_format" in kwargs:
            sym_map = SymbolApi(
                get_api_client()
            ).id_convert_create(
                _from="id",
                to=kwargs["code_format"],
                source=",".join(str(c) for c in df.columns)
            ).code_mapped
            df.columns = [str(c) for c in df.columns]
            df.rename(columns=sym_map, inplace=True)
            df = df.loc[:, ~df.columns.isna()]

        return df
