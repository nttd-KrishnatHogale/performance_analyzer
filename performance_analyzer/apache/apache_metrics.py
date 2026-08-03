import pandas as pd


class ApacheMetrics:

    def worker_utilization(self, modstatus_df):

        if modstatus_df is None:

            return None

        if modstatus_df.empty:

            return None

        df = modstatus_df.copy()

        df["worker_utilization"] = (

            df["busyworkers"] /

            df["workerssum"]

        ) * 100

        return df

    def error_rate(self, throughput_df):

        if throughput_df is None:

            return None

        if throughput_df.empty:

            return None

        df = throughput_df.copy()

        df["is_error"] = df["status"] >= 500

        return (

            df

            .resample("1min")

            .agg(

                errors=("is_error","sum"),

                total=("status","count")

            )

        )

    def latency(self, throughput_df):

        if throughput_df is None:

            return None

        if throughput_df.empty:

            return None

        return (

            throughput_df

            .resample("1min")

            .agg(

                latency=("response_time","mean"),

                p95=("response_time",lambda x:x.quantile(.95))

            )

        )

    def throughput(self, throughput_df):

        if throughput_df is None:

            return None

        if throughput_df.empty:

            return None

        return (

            throughput_df

            .resample("1min")

            .size()

            .rename("rps")
            .to_frame()
        )