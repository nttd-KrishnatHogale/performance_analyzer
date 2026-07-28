from performance_analyzer.anomaly_detection.metric_resolver import get_metric_columns
from performance_analyzer.anomaly_detection.metric_constants import CPU_USAGE
import numpy as np

def detect_patterns(df, results):

    # -----------------------------
    # CPU sustained high
    # -----------------------------
    cpu_cols = get_metric_columns(df, CPU_USAGE)

    for col in cpu_cols:
        high = (df[col] > 70).sum()

        if high > 5:
            results["patterns"].append(
                f"{col} sustained high usage"
            )

    # -----------------------------
    # Increasing trend
    # -----------------------------
    for col in df.columns:

        if df[col].dtype not in ["float64", "int64"]:
            continue

        series = df[col].dropna()

        if len(series) < 10:
            continue

        slope = np.polyfit(range(len(series)), series, 1)[0]

        if slope > 0.5:
            results["patterns"].append(f"{col} increasing trend")
