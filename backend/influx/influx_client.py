from influxdb import InfluxDBClient

from config.config_service import ConfigService
from backend.utils.logger import Logger


logger = Logger.get_logger()


class InfluxService:

    def __init__(self):

        config = ConfigService()

        self.client = InfluxDBClient(
            host=config.get("influxdb.host"),
            port=config.get("influxdb.port"),
            username=config.get("influxdb.username"),
            password=config.get("influxdb.password"),
            database=config.get("influxdb.database"),
        )

    def ping(self):

        return self.client.ping()
    def query(self, measurement, start_time, end_time):

        query = f"""
        SELECT *
        FROM "{measurement}"
        WHERE time >= '{start_time}'
        AND time <= '{end_time}'
        """

        logger.info("=" * 60)
        logger.info(f"Measurement : {measurement}")
        logger.info(f"Start Time  : {start_time}")
        logger.info(f"End Time    : {end_time}")
        logger.info(query)
        logger.info("=" * 60)

        result = self.client.query(query)

        rows = list(result.get_points(measurement=measurement))

        logger.info(f"InfluxDB Query Successful : {measurement}")
        logger.info(f"{measurement} -> {len(rows)} rows fetched")

        return rows