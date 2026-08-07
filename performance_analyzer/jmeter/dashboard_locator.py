from pathlib import Path


class DashboardLocator:

    @staticmethod
    def latest_dashboard(report_root: str):

        report_root = Path(report_root)

        dashboards = [
            d for d in report_root.iterdir()
            if d.is_dir() and d.name.endswith("_dashboard")
        ]

        if not dashboards:
            raise FileNotFoundError(
                f"No JMeter dashboards found in {report_root}"
            )

        dashboards.sort(
            key=lambda d: d.stat().st_mtime,
            reverse=True
        )

        latest = dashboards[0]

        # print(f"Using dashboard: {latest}")

        return latest