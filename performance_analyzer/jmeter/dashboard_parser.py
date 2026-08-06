import json
from pathlib import Path


class DashboardParser:

    def parse(self, dashboard_folder):

        dashboard_folder = Path(dashboard_folder)

        statistics_file = dashboard_folder / "statistics.json"

        if not statistics_file.exists():
            raise FileNotFoundError(statistics_file)

        with open(statistics_file, "r", encoding="utf-8") as f:
            statistics = json.load(f)

        return statistics