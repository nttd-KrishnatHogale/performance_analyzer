from pathlib import Path
import logging


class Logger:

    _logger = None

    @staticmethod
    def get_logger():

        if Logger._logger:

            return Logger._logger

        Path("logs").mkdir(exist_ok=True)

        logger = logging.getLogger("PerformancePlatform")

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        file_handler = logging.FileHandler(

            "logs/application.log"

        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        Logger._logger = logger

        return logger