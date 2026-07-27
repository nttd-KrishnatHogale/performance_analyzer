import numpy as np


def detect_anomalies(df, results):

    for col in df.columns:

        if not np.issubdtype(df[col].dtype, np.number):
            continue

        series = df[col].dropna()

        if len(series) < 20:
            continue

        std = series.std()
        if std == 0:
            continue

        mean = series.mean()
        z_scores = (series - mean) / std

        anomalies = z_scores[abs(z_scores) > 2]

        for t, z in anomalies.items():
            value = series.loc[t]

            results["anomalies"].append(
                f"{col} anomaly at {t} (value={value:.2f}, z={z:.2f})"
            )
