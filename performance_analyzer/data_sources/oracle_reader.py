from influxdb import InfluxDBClient
import pandas as pd


class OracleReader:

    def __init__(self):
        config = __import__('performance_analyzer.config.settings', fromlist=[''])
        self.client = InfluxDBClient(
            host=config.INFLUX_HOST,
            port=config.INFLUX_PORT,
            username=config.INFLUX_USERNAME,
            password=config.INFLUX_PASSWORD,
            database=config.INFLUX_DB
        )

    def query_df(self, query):
        result = self.client.query(query)
        df = pd.DataFrame(list(result.get_points()))

        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], utc=True)
            df.set_index('time', inplace=True)

        return df

    def load_all(self, start_time, end_time, hostname, sid):

        base = f"""WHERE time >= '{start_time}' AND time <= '{end_time}' AND hostname = '{hostname}' AND sid = '{sid}'"""

        data = {}

        data["count_stats"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_count_statistics" {base}
        """)

        data["timed"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_timed" {base}
        """)

        data["efficiency"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_efficiency" {base}
        """)

        data["time_model"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_time_model_statistics" {base}
        """)

        data["sql_stats"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_stats" {base}
        """)

        data["pga"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_pga" {base}
        """)

        data["sga"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_sga" {base}
        """)

        data["shared_pool"] = self.query_df(f"""
            SELECT * FROM "rp_summary"."oracle_sql_shared_pool" {base}
        """)
        # NEW: Load execution plans
        data["plan"] = self.query_df(f"""
            SELECT *
            FROM "rp_summary"."oracle_sql_plan"
            {base}
        """)
        return data