import pandas as pd


class JMeterAnalyzer:

    def analyze(self, df):

        if df is None or df.empty:
            return {}

        report = {}

        # Overall statistics
        report["total_requests"] = len(df)

        report["avg_response_time"] = float(df["elapsed"].mean())

        report["p90_response_time"] = float(df["elapsed"].quantile(0.90))

        report["max_response_time"] = float(df["elapsed"].max())

        # Error rate
        if "success" in df.columns:
            report["error_rate"] = (
                (~df["success"]).mean() * 100
            )

        # Transaction-wise summary
        if "label" in df.columns:

            report["transactions"] = []

            grouped = df.groupby("label")

            for name, group in grouped:

                report["transactions"].append({

                    "transaction": name,

                    "avg": float(group["elapsed"].mean()),

                    "p90": float(group["elapsed"].quantile(0.90)),

                    "max": float(group["elapsed"].max()),

                    "count": len(group)

                })

        return report