def merge_dataframes(df_list):
    """
    Safely merge multiple DataFrames on time index
    """

    dfs = [df for df in df_list if df is not None and not df.empty]

    if not dfs:
        return None

    combined = dfs[0]

    for df in dfs[1:]:

        overlap = combined.columns.intersection(df.columns)
        df = df.drop(columns=overlap, errors="ignore")

        combined = combined.join(df, how="outer")

    combined.sort_index(inplace=True)
    combined.fillna(0, inplace=True)

    return combined