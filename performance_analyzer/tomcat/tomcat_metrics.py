import pandas as pd


class TomcatMetrics:

    # -------------------------
    # Heap Utilization
    # -------------------------

    def heap_usage(self, jvm_df):

        if jvm_df is None or jvm_df.empty:
            return None

        df = jvm_df.copy()

        df["heap_used_pct"] = (
            df["heap_total"] /
            df["opt_mx"]
        ) * 100

        return df

    # -------------------------
    # GC Throughput
    # -------------------------

    def gc(self, jvm_df):

        if jvm_df is None or jvm_df.empty:
            return None

        return jvm_df.copy()

    # -------------------------
    # Thread Pool
    # -------------------------

    def thread_utilization(self, thread_df):

        if thread_df is None or thread_df.empty:
            return None

        df = thread_df.copy()

        if (
            "currentThreadsBusy" in df.columns and
            "maxThreads" in df.columns
        ):

            df["thread_utilization"] = (

                df["currentThreadsBusy"] /

                df["maxThreads"]

            ) * 100

        return df

    # -------------------------
    # JDBC Pool
    # -------------------------

    def jdbc_pool(self, ds_df):

        if ds_df is None or ds_df.empty:
            return None

        df = ds_df.copy()

        if (
            "numActive" in df.columns and
            "maxActive" in df.columns
        ):

            df["jdbc_utilization"] = (

                df["numActive"] /

                df["maxActive"]

            ) * 100

        return df

    # -------------------------
    # Sessions
    # -------------------------

    def sessions(self, session_df):

        if session_df is None or session_df.empty:
            return None

        return session_df.copy()