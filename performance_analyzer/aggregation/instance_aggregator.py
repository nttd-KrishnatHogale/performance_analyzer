import pandas as pd


def aggregate_instance_df(df):
    """
    Standardize any time-series dataframe
    """

    if df is None or df.empty:
        return None

    df = df.apply(pd.to_numeric, errors="coerce")

    # Align time
    df = df.resample("1min").mean()

    # Smooth missing
    df.fillna(method="ffill", inplace=True)
    df.fillna(0, inplace=True)

    return df