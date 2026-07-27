from influxdb import InfluxDBClient
import pandas as pd
from backend.utils.logger import Logger

logger = Logger.get_logger()
# This class is responsible for connecting to InfluxDB and querying the required metrics.
class InfluxReader:
    # Initialize the InfluxDB client using the provided configuration.
    def __init__(self):
        config = __import__('config.settings', fromlist=[''])
        self.client = InfluxDBClient(
            host=config.INFLUX_HOST,
            port=config.INFLUX_PORT,
            username=config.INFLUX_USERNAME,
            password=config.INFLUX_PASSWORD,
            database=config.INFLUX_DB
        )
    
    # Query CPU metrics from InfluxDB for the specified time range.
    def query_cpu(self, start, end, hostname):
        query = f"""
            SELECT 
                dstat__total_cpu_usage__hiq, 
                dstat__total_cpu_usage__idl, 
                dstat__total_cpu_usage__siq, 
                dstat__total_cpu_usage__stl, 
                dstat__total_cpu_usage__sys, 
                dstat__total_cpu_usage__usr, 
                dstat__total_cpu_usage__wai 
            FROM 
                "rp_oslinux_detail"."oslinux_dstat_base"
            WHERE time >= '{start}' AND time <= '{end}' AND hostname = '{hostname}'
            """
        logger.info("=" * 80)
        logger.info("PERFORMANCE ANALYZER - CPU QUERY")
        logger.info(f"Hostname   : {hostname}")
        logger.info(f"Start Time : {start}")
        logger.info(f"End Time   : {end}")
        logger.info(query)
        result = self.client.query(query)
        return pd.DataFrame(list(result.get_points()))

    # Query Memory metrics from InfluxDB for the specified time range.
    def query_memory(self, start, end, hostname):
        query = f"""
            SELECT 
                dstat__memory_usage__buff, 
                dstat__memory_usage__cach, 
                dstat__memory_usage__free, 
                dstat__memory_usage__used 
            FROM 
                "rp_oslinux_detail"."oslinux_dstat_base"
            WHERE time >= '{start}' AND time <= '{end}' AND hostname = '{hostname}'
            """
        result = self.client.query(query)
        return pd.DataFrame(list(result.get_points()))