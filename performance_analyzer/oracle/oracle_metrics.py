import pandas as pd


class OracleMetrics:

    def top_elapsed_sql(self, sql_df):

        if sql_df is None or sql_df.empty:
            return None

        return (

            sql_df

            .sort_values(

                "elapsed_time",

                ascending=False

            )

        )

    def top_cpu_sql(self, timed_df):

        if timed_df is None or timed_df.empty:
            return None

        if "db_cpu" not in timed_df.columns:

            return None

        return (

            timed_df

            .sort_values(

                "db_cpu",

                ascending=False

            )

        )

    def top_waits(self, efficiency_df):

        if efficiency_df is None or efficiency_df.empty:

            return None

        return efficiency_df

    def connection_statistics(self, count_df):

        if count_df is None or count_df.empty:

            return None

        return count_df

    def execution_rate(self, sql_df):

        if sql_df is None or sql_df.empty:

            return None

        if "executions" not in sql_df.columns:

            return None

        return sql_df