import os
import socket
import requests

from influxdb import InfluxDBClient

from config.config_service import ConfigService
from backend.database.database import Database
from backend.utils.logger import Logger
from sqlalchemy import text


logger = Logger.get_logger()


class ConnectionChecker:

    def __init__(self):

        self.config = ConfigService()

    # --------------------------------------------------
    # SQLite
    # --------------------------------------------------

    def check_database(self):

        try:

            session = Database.get_session()

            # session.execute("SELECT 1")
            session.execute(text("SELECT 1"))

            session.close()

            return True, "Connected"

        except Exception as e:

            logger.exception(e)

            return False, str(e)

    # --------------------------------------------------
    # InfluxDB
    # --------------------------------------------------

    def check_influx(self):

        try:

            client = InfluxDBClient(
                host=self.config.get("influxdb.host"),
                port=self.config.get("influxdb.port"),
                username=self.config.get("influxdb.username"),
                password=self.config.get("influxdb.password"),
                database=self.config.get("influxdb.database"),
            )

            version = client.ping()

            return True, f"InfluxDB ({version})"

        except Exception as e:

            logger.exception(e)

            return False, str(e)

    # --------------------------------------------------
    # JMeter
    # --------------------------------------------------

    def check_jmeter(self):

        path = self.config.get("jmeter.executable")

        if os.path.exists(path):

            return True, path

        return False, "JMeter executable not found"

    # --------------------------------------------------
    # Application URL
    # --------------------------------------------------

    def check_application(self):

        url = self.config.get("application.url")
        logger.info(f"Checking application URL: {url}")

        try:

            response = requests.get(
                url,
                timeout=10
            )
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Final URL: {response.url}")
            if response.status_code == 200:

                return True, "Application Reachable"

            return False, f"HTTP {response.status_code}"

        except Exception as e:

            logger.exception(e)

            return False, str(e)

    # --------------------------------------------------
    # Ping Linux Server
    # --------------------------------------------------

    def check_linux_server(self):

        host = self.config.get("application.host")

        try:

            socket.create_connection(
                (host, 22),
                timeout=5
            )

            return True, "SSH Port Reachable"

        except Exception as e:

            return False, str(e)

    # --------------------------------------------------
    # Run All Checks
    # --------------------------------------------------

    def run_all(self):

        return {

            "Database": self.check_database(),

            "InfluxDB": self.check_influx(),

            "JMeter": self.check_jmeter(),

            "Application": self.check_application(),

            "Linux Server": self.check_linux_server(),

        }