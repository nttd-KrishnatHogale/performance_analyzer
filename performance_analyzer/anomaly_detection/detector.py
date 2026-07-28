from performance_analyzer.anomaly_detection.anomaly_utils import detect_anomalies
from performance_analyzer.anomaly_detection.pattern_utils import detect_patterns
from performance_analyzer.anomaly_detection.violation_utils import detect_violations
from performance_analyzer.anomaly_detection.correlation_utils import detect_correlations


def analyze_dataframe(df):

    results = {
        "anomalies": [],
        "patterns": [],
        "violations": [],
        "correlations": []
    }

    if df is None or df.empty:
        return results

    # ✅ Debug (keep during development)
    # print(f"\nProcessing DataFrame with {len(df.columns)} columns")

    # ----------------------------------------------------
    # APPLY DETECTORS
    # ----------------------------------------------------
    detect_anomalies(df, results)
    detect_patterns(df, results)
    detect_violations(df, results)
    detect_correlations(df, results)

    return results

def detect_anomalies_and_patterns(aggregated_data):

    analysis_results = {
        "flows": {},
        "servers": {}
    }

    # ✅ FLOW LEVEL
    for flow_id, df in aggregated_data["flows"].items():
        analysis_results["flows"][flow_id] = analyze_dataframe(df)

    # ✅ SERVER LEVEL
    for server, df in aggregated_data["servers"].items():
        analysis_results["servers"][server] = analyze_dataframe(df)

    return analysis_results