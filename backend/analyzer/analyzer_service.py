"""
backend/analyzer/analyzer_service.py
"""

from pathlib import Path
from datetime import datetime

from backend.database.repository import TestRunRepository
from backend.orchestrator.status_manager import status_manager
from backend.utils.logger import Logger
from performance_analyzer.Main import run_analysis
from performance_analyzer.config import settings

logger = Logger.get_logger()


class AnalyzerService:

    def __init__(self):
        pass

    def run(
        self,
        run_id: int,
        jtl_file: str,
        runtime_directory: str,
        start_time,
        end_time,

    ):

        logger.info("Starting Performance Analyzer")
        settings.START_TIME = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        settings.END_TIME = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        status_manager.update(
            stage="Performance Analysis",
            progress=97,
            message="Running Performance Analyzer..."
        )
        logger.info("========== PERFORMANCE ANALYZER ==========")
        logger.info(f"Start Time : {start_time}")
        logger.info(f"End Time   : {end_time}")
        logger.info("==========================================")
        logger.info("=" * 80)
        logger.info("Performance Analyzer Invoked")
        logger.info("=" * 80)
        try:

            # -----------------------------------------------------
            # TODO
            # Replace this section with your existing
            # PerformanceAnalyzer invocation.
            #
            # Example:
            #
            # analyzer = PerformanceAnalyzer(...)
            # analyzer.execute()
            #
            # -----------------------------------------------------
            # analyzer = PerformanceAnalyzer(
            #     jmeter_file=jtl_file,
            #     runtime_directory=runtime_directory,
            #     output_directory=report_directory
            # )
            logger.info("Calling performance_analyzer.Main.run_analysis()")
            run_analysis(
                config_path="performance_analyzer/config/monitoring_config.yaml",run_id=run_id
                    # start_time=start_time,
                    # end_time=end_time
            )
            # analyzer.run()           

            report_directory = Path("reports") / str(run_id)
            report_directory.mkdir(
                parents=True,
                exist_ok=True
            )
            generated_html = Path("output") / "flow_1_report.html"
            # html_report = report_directory / "report.html"
            html_report = report_directory / "report.html"
            # json_report = report_directory / "report.json"
            import shutil
            shutil.copy2(generated_html, html_report)

            json_report = ""
            #
            # Temporary placeholder until PerformanceAnalyzer
            # is integrated.
            #

            # html_report.write_text(
            #     "<html><body><h1>Performance Report</h1></body></html>"
            # )

            # json_report.write_text(
            #     '{"status":"completed"}'
            # )

            TestRunRepository.update_report(
                run_id=run_id,
                html_report=str(html_report),
                json_report=str(json_report)
            )

            status_manager.update(
                stage="Reports Generated",
                progress=99,
                message="Reports generated successfully."
            )
            logger.info("Performance Analyzer Completed Successfully")
            logger.info("Performance Analyzer completed.")

            return {
                "success": True,
                "html": str(html_report),
                "json": str(json_report)
            }

        except Exception as ex:

            logger.exception(ex)

            status_manager.failed(str(ex))

            TestRunRepository.complete_run(
                run_id=run_id,
                end_time=datetime.now(),
                status="FAILED"
            )

            return {
                "success": False,
                "error": str(ex)
            }