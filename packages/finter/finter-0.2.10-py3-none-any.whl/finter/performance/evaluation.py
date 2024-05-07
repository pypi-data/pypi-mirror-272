from finter.settings import get_api_client
from finter.data import ModelData, DB
from finter.data import Symbol

from datetime import datetime
import pandas as pd


class Evaluator:
    @staticmethod
    def top_n_assets(position, n, start=None, end=None, universe=0):
        """
        Retrieves the top n assets based on returns within a specified time frame.
        Args:
            position (str or DataFrame): The position data source or DataFrame.
            n (int): The number of top assets to retrieve.
            start (int, optional): The start date in YYYYMMDD format.
            end (int, optional): The end date in YYYYMMDD format.
            universe (int): Indicates the universe from which to pull data.
        Returns:
            DataFrame: The top n assets sorted by their returns.
        Raises:
            ValueError: If the input parameters are not as expected.
        """
        if not isinstance(position, (str, pd.DataFrame)):
            raise ValueError(
                "The 'position' parameter must be either a string or a pandas DataFrame."
            )

        # Load and preprocess position data
        if isinstance(position, str):
            model_info = position.split(".")
            position = ModelData.load(position)
        if isinstance(position.columns[0], str) and not model_info[2] == "compustat":
            position.columns = position.columns.astype(int)

        start, end = Evaluator._parse_edge_dates(start, end)
        position = position.loc[start:end]
        position = position.shift(1)

        # Load price and adjust factor
        raw, adj = Evaluator._load_adjusted_prices(position.columns, model_info)
        raw, adj = raw.loc[start:end], adj.loc[start:end]
        sum_chg, top_n_indices = Evaluator._calculate_cumsum_n_indicies(
            position, n, raw, adj
        )

        if model_info[1] == "krx" and model_info[3] == "future_0":
            mapping = ModelData.load(
                "content.krx.quantize.universe.equity_futures_entity_id_to_underlying_stock_ccid.1d"
            )
            mapping = mapping.mode()
            mapping = mapping.astype(int)
            ccid_dict = mapping.iloc[0][top_n_indices].to_dict()
            ccid_dict = {str(v): str(k) for k, v in ccid_dict.items()}
            ret_dict = sum_chg[top_n_indices].to_dict()
            ret_dict = {str(k): v for k, v in ret_dict.items()}
            top_n_indices = list(ccid_dict.keys())

        # Get entity_name from ccid or entity_id
        if model_info[1] == "krx":
            # Convert symbol IDs to entity names
            mapped = Symbol.convert(
                _from="id", to="entity_name", source=list(top_n_indices)
            )
            if model_info[3] == "future_0":
                return Evaluator._krx_future_mapper(mapped, ccid_dict, ret_dict)
            else:
                return Evaluator._krx_spot_mapper(mapped, sum_chg, False)

        # Make the result DataFrame for us model
        elif model_info[1] == "us":
            if model_info[2] == "compustat":
                return Evaluator._us_spglobal_mapper(sum_chg, top_n_indices)
            elif model_info[2] == "us":
                return Evaluator._us_factset_mapper(sum_chg, top_n_indices)

    @staticmethod
    def bottom_n_assets(position, n, start=None, end=None, universe=0):
        """
        Retrieves the bottom n assets based on returns within a specified time frame.
        Args:
            position (str or DataFrame): The position data source or DataFrame.
            n (int): The number of bottom assets to retrieve.
            start (int, optional): The start date in YYYYMMDD format.
            end (int, optional): The end date in YYYYMMDD format.
            universe (int): Indicates the universe from which to pull data.
        Returns:
            DataFrame: The bottom n assets sorted by their returns.
        Raises:
            ValueError: If the input parameters are not as expected.
        """

        if not isinstance(position, (str, pd.DataFrame)):
            raise ValueError(
                "The 'position' parameter must be either a string or a pandas DataFrame."
            )

        # Load and preprocess position data
        if isinstance(position, str):
            model_info = position.split(".")
            position = ModelData.load(position)
        if isinstance(position.columns[0], str) and not model_info[2] == "compustat":
            position.columns = position.columns.astype(int)

        start, end = Evaluator._parse_edge_dates(start, end)
        position = position.loc[start:end]
        position = position.shift(1)

        # Load price and adjust factor
        raw, adj = Evaluator._load_adjusted_prices(position.columns, model_info)
        raw, adj = raw.loc[start:end], adj.loc[start:end]
        sum_chg, bottom_n_indices = Evaluator._calculate_cumsum_n_indicies(
            position, n, raw, adj, True
        )

        if model_info[1] == "krx" and model_info[3] == "future_0":
            mapping = ModelData.load(
                "content.krx.quantize.universe.equity_futures_entity_id_to_underlying_stock_ccid.1d"
            )
            mapping = mapping.mode()
            mapping = mapping.astype(int)
            ccid_dict = mapping.iloc[0][bottom_n_indices].to_dict()
            ccid_dict = {str(v): str(k) for k, v in ccid_dict.items()}
            ret_dict = sum_chg[bottom_n_indices].to_dict()
            ret_dict = {str(k): v for k, v in ret_dict.items()}
            bottom_n_indices = list(ccid_dict.keys())

        # Get entity_name from ccid or entity_id
        if model_info[1] == "krx":
            # Convert symbol IDs to entity names
            mapped = Symbol.convert(
                _from="id", to="entity_name", source=list(bottom_n_indices)
            )
            if model_info[3] == "future_0":
                return Evaluator._krx_future_mapper(mapped, ccid_dict, ret_dict, True)
            else:
                return Evaluator._krx_spot_mapper(mapped, sum_chg, True)

        # Make the result DataFrame for us model
        elif model_info[1] == "us":
            if model_info[2] == "compustat":
                return Evaluator._us_spglobal_mapper(sum_chg, bottom_n_indices, True)
            elif model_info[2] == "us":
                return Evaluator._us_factset_mapper(sum_chg, bottom_n_indices, True)

    @staticmethod
    def _load_adjusted_prices(position_column, model_info):
        """
        Load adjusted prices based on the market and the type of security.
        Args:
            position_column (str): The column from the DataFrame to be adjusted.
            model_info (list): Information about the market and security type.
        Returns:
            tuple: Tuple containing DataFrames for raw and adjusted prices.
        """
        if model_info[1] == "krx":
            if model_info[3] == "future_0":
                raw = ModelData.load(
                    "content.krx.live.price_volume.stock-future_0-price_close.1d"
                )
                adj = ModelData.load(
                    "content.krx.live.cax.stock-future-adjust_factor.1d"
                )
            else:
                raw = ModelData.load(
                    "content.handa.dataguide.price_volume.krx-spot-price_close.1d"
                )
                adj = ModelData.load(
                    "content.handa.dataguide.cax.krx-spot-adjust_factor.1d"
                )
        elif model_info[1] == "us":
            if model_info[2] == "compustat":
                raw = ModelData.load(
                    "content.spglobal.compustat.price_volume.us-all-price_close.1d"
                )
                adj = ModelData.load(
                    "content.spglobal.compustat.cax.us-all-adjust_factor.1d"
                )
            elif model_info[2] == "us":
                if model_info[3] == "etf":
                    raw = ModelData.load(
                        "content.factset.api.price_volume.us-etf-price_close.1d"
                    )
                    adj = ModelData.load(
                        "content.factset.api.cax.us-etf-adjust_factor.1d"
                    )
                elif model_info[3] == "stock":
                    raw = ModelData.load(
                        "content.factset.api.price_volume.us-stock-price_close.1d"
                    )
                    adj = ModelData.load(
                        "content.factset.api.cax.us-stock-adjust_factor.1d"
                    )
        raw = raw[position_column]
        adj = adj[position_column]
        return raw, adj

    @staticmethod
    def _parse_edge_dates(start, end):
        """
        Converts integer dates to formatted string dates.
        Args:
            start (int): Start date in YYYYMMDD format.
            end (int): End date in YYYYMMDD format.
        Returns:
            tuple: Tuple containing formatted string dates.
        """
        if start:
            if isinstance(start, int):
                start = str(start)
                date_object = datetime.strptime(start, "%Y%m%d")
                start = date_object.strftime("%Y-%m-%d")
            else:
                raise ValueError(
                    "The 'start' parameter must be integers in YYYYMMDD format. For example, 20000101."
                )
        if end:
            if isinstance(end, int):
                end = str(end)
                date_object = datetime.strptime(end, "%Y%m%d")
                end = date_object.strftime("%Y-%m-%d")
            else:
                raise ValueError(
                    "The 'end' parameter must be integers in YYYYMMDD format. For example, 20000101."
                )
        return start, end

    @staticmethod
    def _calculate_cumsum_n_indicies(position, n, raw, adj, bottom=False):
        """
        Calculate the cumulative sum of changes and select the top/bottom n indices.
        Args:
            position (DataFrame): Position data for calculating weights.
            n (int): Number of indices to select.
            raw (DataFrame): Raw price data.
            adj (DataFrame): Adjustment factors.
            bottom (bool): Flag to choose bottom n if True, else top n.
        Returns:
            DataFrame: Top or bottom n indices based on the cumulative sum of changes.
        """
        # Calculate daily returns
        chg = (raw * adj).pct_change()

        # Apply position weights
        mask = position / 1e8
        chg *= mask
        chg.fillna(0, inplace=True)

        # Calculate sum of returns and filter only assets with non-zero total position
        sum_chg = chg.sum()

        # Filter only assets with non-zero total position
        valid_assets = position.sum()[position.sum() > 0].index
        sum_chg = sum_chg[sum_chg.index.isin(valid_assets)]

        # Select top n assets
        if bottom:
            n_indices = sum_chg.nsmallest(min(n, len(sum_chg))).index
        else:
            n_indices = sum_chg.nlargest(min(n, len(sum_chg))).index

        return sum_chg, n_indices

    @staticmethod
    def _krx_spot_mapper(mapped, sum_chg, bottom=False):
        """
        Maps and sorts KRX spot data for visualization.
        Args:
            mapped (dict): Mapping from IDs to entity names.
            sum_chg (Series): Cumulative changes for each entity.
            bottom (bool): Sort ascending if True.
        Returns:
            DataFrame: Sorted DataFrame with entity names as indices.
        """
        df = pd.DataFrame(
            {"ret": sum_chg.loc[list(map(int, mapped.keys()))]}
        ).sort_values(by="ret", ascending=bottom)
        df.index = df.index.map(str)
        df["entity_name"] = df.index.map(mapped)
        df.set_index("entity_name", inplace=True)
        return df

    @staticmethod
    def _krx_future_mapper(mapped, ccid_dict, ret_dict, bottom=False):
        """
        Maps and sorts KRX future data for visualization.
        Args:
            mapped (dict): Mapping from IDs to entity names.
            ccid_dict (dict): Mapping from future indices to underlying stock CCIDs.
            ret_dict (dict): Cumulative changes for each future index.
            bottom (bool): Sort ascending if True.
        Returns:
            DataFrame: Sorted DataFrame with entity names as indices.
        """
        mapped_reverse = {v: k for k, v in mapped.items()}
        result = pd.DataFrame(
            index=mapped.values(), columns=["ret", "ccid", "entity_id"]
        )
        result["ccid"] = result.index.map(mapped_reverse)
        result["entity_id"] = result["ccid"].map(ccid_dict)
        result["ret"] = result["entity_id"].map(ret_dict)
        df = result.sort_values(by="ret", ascending=bottom)
        return df

    @staticmethod
    def _us_spglobal_mapper(sum_chg, indices, bottom=False):
        """
        Maps and sorts S&P Global data for visualization.
        Args:
            sum_chg (Series): Cumulative changes for each index.
            indices (list): List of indices to include.
            bottom (bool): Sort ascending if True.
        Returns:
            DataFrame: Sorted DataFrame with entity names as indices.
        """
        db = DB("spglobal")
        quoted_ids = ",".join(f"'{id_[:6]}'" for id_ in indices)
        mapped = db.query(f"select * from gic_company WHERE gvkey IN ({quoted_ids})")

        ret_df = pd.DataFrame(
            {
                "gvkeyiid": indices,
                "ret": [sum_chg[idx] for idx in indices],
            }
        )
        ret_df["gvkey"] = ret_df["gvkeyiid"].str[:6]

        df = pd.merge(mapped, ret_df, on="gvkey")[["conm", "ret", "gvkeyiid"]]
        df.rename(columns={"conm": "entity_name"}, inplace=True)
        df.set_index("entity_name", inplace=True)
        df.sort_values("ret", ascending=bottom, inplace=True)
        return df

    @staticmethod
    def _us_factset_mapper(sum_chg, indices, bottom=False):
        """
        Maps and sorts FactSet data for visualization.
        Args:
            sum_chg (Series): Cumulative changes for each index.
            indices (list): List of indices to include.
            bottom (bool): Sort ascending if True.
        Returns:
            DataFrame: Sorted DataFrame with entity names as indices.
        """
        ret_dict = dict(sum_chg[indices])
        mapped_ccid = Symbol.convert(_from="id", to="entity_name", source=list(indices))
        quoted_ids = ",".join(f"'{id_}'" for id_ in list(mapped_ccid.values()))

        db = DB("factset")
        mapper = db.query(
            f"SELECT * FROM sym_v1_sym_entity WHERE factset_entity_id IN ({quoted_ids})"
        )
        mapper = mapper[["factset_entity_id", "entity_proper_name"]]

        tmp_df = pd.DataFrame(
            list(mapped_ccid.items()), columns=["ccid", "factset_entity_id"]
        )
        ret_df = pd.DataFrame(list(ret_dict.items()), columns=["ccid", "ret"]).astype(
            {"ccid": str}
        )

        # Merge the DataFrames to combine all the necessary information
        merged_df = ret_df.merge(tmp_df, on="ccid").merge(
            mapper, on="factset_entity_id"
        )

        # Set the index to 'entity_proper_name' and select the final columns for output
        df = merged_df.set_index("entity_proper_name")[["ret", "ccid"]]
        df.sort_values(by="ret", ascending=bottom, inplace=True)

        return df
