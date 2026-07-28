import pandas as pd
from performance_analyzer.aggregation.merge_utils import merge_dataframes


def aggregate_oracle_instance(db_data):
    """
    Merge all Oracle tables into single DF
    """

    if db_data is None:
        return None

    dfs = []

    for name, df in db_data.items():

        if df is None or df.empty:
            continue

        df = df.apply(pd.to_numeric, errors="coerce")
        df = df.resample("1min").mean()

        dfs.append(df)

    return merge_dataframes(dfs)