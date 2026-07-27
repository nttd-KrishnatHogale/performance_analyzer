"""
backend/storage/metric_storage.py

Stores runtime metrics collected from InfluxDB.
"""

from pathlib import Path

import pandas as pd

from config.config_service import ConfigService
from backend.utils.logger import Logger

logger = Logger.get_logger()

# class MetricStorage:

#     def __init__(self):
#         config = ConfigService()


#         # self.folder = Path("reports/runtime")
#         self.output_directory = config.get(
#             "runtime.save_directory",
#             "reports/runtime"
#         )

#         # self.folder.mkdir(
#         #     parents=True,
#         #     exist_ok=True
#         # )
#         self.output_directory = Path(self.output_directory)

#         self.output_directory.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#     def append(self, measurement, rows):

#         if not rows:
#             return

#         file = self.folder / f"{measurement}.csv"

#         df = pd.DataFrame(rows)

#         if file.exists():

#             df.to_csv(
#                 file,
#                 mode="a",
#                 header=False,
#                 index=False
#             )

#         else:

#             df.to_csv(
#                 file,
#                 index=False
#             )

class MetricStorage:

    def __init__(self):

        config = ConfigService()

        self.output_directory = config.get(
            "runtime.save_directory",
            "reports/runtime"
        )

        self.output_directory = Path(self.output_directory)

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def append(
        self,
        metric_name: str,
        data
    ):

        if data is None:
            return

        if isinstance(data, list):
            if len(data) == 0:
                return
            df = pd.DataFrame(data)

        elif isinstance(data, pd.DataFrame):
            if data.empty:
                return
            df = data.copy()

        else:
            logger.warning(
                f"Unsupported data type for {metric_name}"
            )
            return

        file_path = self.output_directory / f"{metric_name}.csv"

        write_header = not file_path.exists()

        df.to_csv(
            file_path,
            mode="a",
            header=write_header,
            index=False
        )

        logger.info(
            f"{len(df)} {metric_name} records appended to {file_path.name}"
        )

    def clear(self):

        for csv_file in self.output_directory.glob("*.csv"):
            csv_file.unlink()

        logger.info("Runtime metric files removed.")

    def get_metric_file(
        self,
        metric_name: str
    ):

        return self.output_directory / f"{metric_name}.csv"

    def metric_exists(
        self,
        metric_name: str
    ) -> bool:

        return self.get_metric_file(metric_name).exists()

    def list_metric_files(self):

        return list(
            self.output_directory.glob("*.csv")
        )