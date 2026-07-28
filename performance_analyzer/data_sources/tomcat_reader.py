from influxdb import InfluxDBClient
import pandas as pd

class TomcatReader:

    def __init__(self):
        config = __import__('performance_analyzer.config.settings', fromlist=[''])
        self.client = InfluxDBClient(
            host=config.INFLUX_HOST,
            port=config.INFLUX_PORT,
            username=config.INFLUX_USERNAME,
            password=config.INFLUX_PASSWORD,
            database=config.INFLUX_DB
        )

    # -----------------------------------------
    # JVM + GC + Heap
    # -----------------------------------------
    def get_jvm_metrics(self, start_time, end_time, hostname, instance):
        query = f"""
        SELECT *
        FROM "rp_tomcat_detail"."java_jmx_tomcat"
        WHERE time >= '{start_time}' AND time <= '{end_time}' AND hostname = '{hostname}' AND instance_name = '{instance}'
        """
        result = self.client.query(query)
        df = pd.DataFrame(list(result.get_points()))

        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], utc=True)
            df.set_index('time', inplace=True)

        return df

    # -----------------------------------------
    # Thread Pool
    # -----------------------------------------
    def get_thread_metrics(self, start_time, end_time, hostname, instance):
        query = f"""
        SELECT *
        FROM "rp_tomcat_detail"."java_jmx_tomcat_thread"
        WHERE time >= '{start_time}' AND time <= '{end_time}' AND hostname = '{hostname}' AND instance_name = '{instance}'
        """
        result = self.client.query(query)
        df = pd.DataFrame(list(result.get_points()))

        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], utc=True)
            df.set_index('time', inplace=True)

        return df

    # -----------------------------------------
    # DB Connection Pool
    # -----------------------------------------
    def get_ds_metrics(self, start_time, end_time, hostname, instance):
        query = f"""
        SELECT *
        FROM "rp_tomcat_detail"."java_jmx_tomcat_ds"
        WHERE time >= '{start_time}' AND time <= '{end_time}' AND hostname = '{hostname}' AND instance_name = '{instance}'
        """
        result = self.client.query(query)
        df = pd.DataFrame(list(result.get_points()))

        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], utc=True)
            df.set_index('time', inplace=True)

        return df

    # -----------------------------------------
    # Sessions
    # -----------------------------------------
    def get_session_metrics(self, start_time, end_time, hostname, instance):
        query = f"""
        SELECT *
        FROM "rp_tomcat_detail"."java_jmx_tomcat_session"
        WHERE time >= '{start_time}' AND time <= '{end_time}' AND hostname = '{hostname}' AND instance_name = '{instance}'
        """
        result = self.client.query(query)
        df = pd.DataFrame(list(result.get_points()))

        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], utc=True)
            df.set_index('time', inplace=True)

        return df
