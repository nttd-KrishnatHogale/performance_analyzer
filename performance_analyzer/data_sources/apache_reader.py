from influxdb import InfluxDBClient
import pandas as pd
from performance_analyzer.config import settings


class ApacheReader:

    def __init__(self):
        self.client = InfluxDBClient(
            host=settings.INFLUX_HOST,
            port=settings.INFLUX_PORT,
            username=settings.INFLUX_USERNAME,
            password=settings.INFLUX_PASSWORD,
            database=settings.INFLUX_DB
        )

    # -----------------------------------------
    # Measurement 1: apache_modstatus
    # -----------------------------------------
    def get_modstatus(self, start_time, end_time, hostname, instance):

        query = f"""
        SELECT 
            time,
            busyworkers,
            workerssum,
            scoreboard_count_cleanup,
            scoreboard_count_closing,
            scoreboard_count_dns,
            scoreboard_count_graceful,
            scoreboard_count_keepalive,
            scoreboard_count_log,
            scoreboard_count_openslot,
            scoreboard_count_read,
            scoreboard_count_reply,
            scoreboard_count_start,
            scoreboard_count_wait
        FROM "rp_apache_modstatus_detail"."apache_modstatus"
        WHERE time >= '{start_time}' AND time <= '{end_time}' AND hostname = '{hostname}' AND instance = '{instance}'
        """

        result = self.client.query(query)
        points = list(result.get_points())

        if not points:
            print("WARNING: No Apache modstatus data found")
            return pd.DataFrame()

        df = pd.DataFrame(points)

        # Ensure time column exists
        if 'time' not in df.columns:
            raise ValueError("Missing 'time' column in apache_modstatus")

        # Convert time to datetime
        df['time'] = pd.to_datetime(df['time'], utc=True)
        df.set_index('time', inplace=True)

        return df

    # -----------------------------------------
    # Measurement 2: apache_throughput (access log)
    # -----------------------------------------
    def get_throughput(self, start_time, end_time, hostname, instance):

        query = f"""
        SELECT 
            time,
            path,
            response_time,
            status,
            size
        FROM "rp_apache_accesslog_detail"."apache_throughput"
        WHERE time >= '{start_time}' AND time <= '{end_time}' AND hostname = '{hostname}' AND instance = '{instance}'
        """

        result = self.client.query(query)
        points = list(result.get_points())

        if not points:
            print("WARNING: No Apache throughput data found")
            return pd.DataFrame()

        df = pd.DataFrame(points)

        # Ensure time column exists
        if 'time' not in df.columns:
            raise ValueError("Missing 'time' column in apache_throughput")

        # Convert time
        df['time'] = pd.to_datetime(df['time'], utc=True)
        df.set_index('time', inplace=True)

        # ✅ Clean important columns (very important for next steps)
        df['response_time'] = pd.to_numeric(df['response_time'], errors='coerce')
        df['status'] = pd.to_numeric(df['status'], errors='coerce')

        # Drop invalid rows
        df.dropna(subset=['response_time'], inplace=True)

        return df
