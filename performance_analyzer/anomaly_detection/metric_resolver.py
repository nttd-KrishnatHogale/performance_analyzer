def get_metric_columns(df, metric_keyword):
    """
    Return all columns containing the metric keyword
    (prefix-safe matching)
    """
    cols = []

    for col in df.columns:
        if metric_keyword.lower() in col.lower():
            cols.append(col)

    return cols
