"""
backend/jmeter/parser.py

JMeter CSV/JTL Parser

Responsible for

• Loading JMeter results
• Validating data
• Timestamp conversion
• Test duration calculation
• Preparing dataframe for analysis
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd

from backend.utils.logger import Logger

@dataclass
class TestMetrics:
    """
    Overall test metrics.
    """

    test_name: str = ""

    start_time: Optional[datetime] = None

    end_time: Optional[datetime] = None

    duration_seconds: float = 0.0

    total_requests: int = 0

    successful_requests: int = 0

    failed_requests: int = 0

    throughput: float = 0.0

    average_latency: float = 0.0

    error_rate: float = 0.0

    dataframe: Optional[pd.DataFrame] = None


@dataclass
class SampleMetrics:
    """
    Metrics for a single sampler.
    """

    label: str

    sample_count: int

    success_count: int

    failure_count: int

    average_time: float

    minimum_time: float

    maximum_time: float

    throughput: float

    error_rate: float


class CSVParser:

    def __init__(self):

        self.logger = Logger.get_logger()

        self.required_columns = [

            "timeStamp",

            "elapsed",

            "label",

            "success"

        ]

    def load_csv(
        self,
        csv_path: str
    ) -> pd.DataFrame:
        """
        Load JMeter CSV/JTL file.
        """

        if not os.path.exists(csv_path):

            raise FileNotFoundError(csv_path)

        self.logger.info(
            f"Loading JMeter results : {csv_path}"
        )

        df = pd.read_csv(
            csv_path,
            low_memory=False
        )

        self.logger.info(
            f"Loaded {len(df)} samples."
        )

        return df
    
    def validate(
        self,
        dataframe: pd.DataFrame
    ):
        """
        Validate required columns.
        """

        missing = []

        for column in self.required_columns:

            if column not in dataframe.columns:

                missing.append(column)

        if missing:

            raise ValueError(

                f"Missing JMeter columns: {missing}"

            )

        self.logger.info(
            "CSV validation successful."
        )

    def convert_timestamp(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Convert epoch milliseconds
        to datetime.
        """

        dataframe["timestamp"] = pd.to_datetime(

            dataframe["timeStamp"],

            unit="ms"

        )

        dataframe = dataframe.sort_values(

            "timestamp"

        )

        dataframe.reset_index(

            drop=True,

            inplace=True

        )

        return dataframe
    
    def determine_test_window(
        self,
        dataframe: pd.DataFrame
    ) -> TestMetrics:
        """
        Determine execution window.
        """

        metrics = TestMetrics()

        metrics.start_time = dataframe[
            "timestamp"
        ].min()

        metrics.end_time = dataframe[
            "timestamp"
        ].max()

        metrics.duration_seconds = (

            metrics.end_time -

            metrics.start_time

        ).total_seconds()

        metrics.total_requests = len(
            dataframe
        )

        metrics.dataframe = dataframe

        self.logger.info(

            f"Execution Window : "

            f"{metrics.start_time}"

            f" -> "

            f"{metrics.end_time}"

        )

        return metrics
    
    def parse(
        self,
        csv_path: str
    ) -> TestMetrics:
        """
        Complete parsing pipeline.
        """

        dataframe = self.load_csv(

            csv_path

        )

        self.validate(

            dataframe

        )

        dataframe = self.convert_timestamp(

            dataframe

        )

        metrics = self.determine_test_window(

            dataframe

        )

        return metrics