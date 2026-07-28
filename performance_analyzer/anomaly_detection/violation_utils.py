from performance_analyzer.anomaly_detection.metric_resolver import get_metric_columns
from performance_analyzer.anomaly_detection.metric_constants import CPU_USAGE


def detect_violations(df, results):

    cpu_cols = get_metric_columns(df, CPU_USAGE)

    for col in cpu_cols:

        violations = (df[col] > 80).sum()

        if violations > 0:
            results["violations"].append(
                f"{col} crossed critical threshold (80%) {violations} times"
            )