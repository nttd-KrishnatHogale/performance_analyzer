# import time
# from datetime import datetime

# from backend.orchestrator.status_manager import status_manager
# from backend.database.repository import TestRunRepository
# from backend.utils.logger import Logger
# from backend.influx.influx_client import InfluxService
# from backend.storage.metric_storage import MetricStorage


# logger = Logger.get_logger()


# class ExecutionMonitor:

#     def __init__(
#         self,
#         process,
#         run,
#         test_run_id
#     ):

#         self.process = process
#         self.run = run
#         self.test_run_id = test_run_id
#         self.influx = InfluxService()

#         self.storage = MetricStorage()
#     def monitor(self):

#         logger.info("Execution Monitor Started")

#         progress = 0

#         while True:

#             if self.process.poll() is not None:
#                 break

#             progress = min(progress + 5, 95)
#             self.start_time = datetime.utcnow().strftime(
#                     "%Y-%m-%dT%H:%M:%SZ"
#                 )

#             cpu = self.influx.query(
#                     "cpu",
#                     self.start_time,
#                     current
#                 )

#             self.storage.append(
#                     "cpu",
#                     cpu
#                 )

#             status_manager.update(
#                 stage="Running JMeter",
#                 progress=progress,
#                 message="Performance Test Running..."
#             )

#             TestRunRepository.update_progress(
#                 self.test_run_id,
#                 progress
#             )

#             logger.info(
#                 f"Execution Running ({progress}%)"
#             )

#             time.sleep(30)

#         logger.info("JMeter Finished")

#         status_manager.complete()

#         TestRunRepository.complete_run(
#             run_id=self.test_run_id,
#             end_time=datetime.now()
#         )

import time
from datetime import datetime

from backend.database.repository import ExecutionLogRepository, TestRunRepository
# from backend.influx.influx_client import InfluxService
from backend.orchestrator.status_manager import status_manager
# from backend.storage.metric_storage import MetricStorage
from backend.utils.logger import Logger
from backend.analyzer.analyzer_service import AnalyzerService

logger = Logger.get_logger()


class ExecutionMonitor:

    def __init__(
        self,
        process,
        run,
        test_run_id,
        start_time=None
    ):

        self.process = process
        self.run = run
        self.test_run_id = test_run_id

        # self.influx = InfluxService()
        # self.storage = MetricStorage()

        if start_time is None:
            start_time = datetime.utcnow()

        self.start_time = start_time
        # self.last_poll_time = start_time

        # Add/remove measurements according to your InfluxDB
        # self.measurements = [
        #     # "cpu",
        #     # "memory",
        #     # "disk",
        #     # "network",
        #     # "apache",
        #     # "tomcat"
        #     "macaDB"
        # ]

    def monitor(self):

        logger.info("Execution Monitor Started")
        logger.info(f"Run ID : {self.test_run_id}")
        logger.info(f"JMeter PID : {self.process.pid}")

        progress = 0

        while True:
            logger.info(f"Checking JMeter process. PID={self.process.pid}")

            # Check whether JMeter is still running
            # if self.process.poll() is not None:
            #     logger.info("JMeter process completed.")
            
            #     break
            # if self.process.poll() is None:

            #     logger.info("JMeter is still running.")

            # else:

            #     logger.info(
            #         f"JMeter finished with Exit Code : {self.process.returncode}"
            #     )
            #     break
            exit_code = self.process.poll()

            logger.info("=" * 50)
            logger.info(f"PID        : {self.process.pid}")
            logger.info(f"poll()     : {exit_code}")
            logger.info(f"returncode : {self.process.returncode}")
            logger.info("=" * 50)

            if exit_code is None:
                logger.info("JMeter is still running.")
            else:
                final_time = datetime.utcnow()

                logger.info(f"JMeter exited with code {exit_code}")
                logger.info(f"Finish Time : {final_time}")

                break
            current_time = datetime.utcnow()

            progress = min(progress + 5, 95)

            status_manager.update(
                status="Running",
                stage="Running JMeter",
                progress=progress,
                message=f"Executing JMeter Test. ({current_time.strftime('%H:%M:%S')})"
            )

            TestRunRepository.update_progress(
                # self.test_run_id,
                # progress
                run_id=self.test_run_id,
                stage="Running JMeter",
                progress=progress,
                status="Running"
            )
            ExecutionLogRepository.add_log(
                    run_id=self.test_run_id,
                    stage="Running JMeter",
                    message=f"Progress updated to {progress}%"
                )
            # Fetch runtime metrics
        #     try:

        #         for measurement in self.measurements:
        #             logger.info(f"Reading measurement : {measurement}")
        #             rows = self.influx.query(
        #                 measurement=measurement,
        #                 start_time=self.last_poll_time,
        #                 end_time=current_time
        #             )

        #             self.storage.append(
        #                 measurement,
        #                 rows
        #             )

        #             # logger.info(
        #             #     f"{measurement}: {len(rows)} rows saved."
        #             # )
        #             logger.info(
        #                 f"{measurement}: {len(rows)} rows fetched from InfluxDB."
        #             )
        #     except Exception as e:

        #         logger.exception(
        #             f"Failed to fetch runtime metrics: {e}"
        #         )

        #     self.last_poll_time = current_time

            logger.info(
                f"Execution Running ({progress}%)"
            )

            time.sleep(5)

        # # Final metric collection
        # logger.info("Collecting final runtime metrics...")

        # try:

        #     final_time = datetime.utcnow()

        #     for measurement in self.measurements:

        #         rows = self.influx.query(
        #             measurement=measurement,
        #             start_time=self.last_poll_time,
        #             end_time=final_time
        #         )

        #         self.storage.append(
        #             measurement,
        #             rows
        #         )

        #         logger.info(
        #             f"Final {measurement}: {len(rows)} rows saved."
        #         )

        # except Exception as e:

        #     logger.exception(
        #         f"Final metric collection failed: {e}"
        #     )

        # -----------------------------
        # Phase 3
        # Run Performance Analyzer here
        #
        # Example:
        #
        # AnalyzerService().run(
        #     jmeter_file=self.run.jtl_file,
        #     runtime_folder="reports/runtime"
        # )
        #
        # -----------------------------


        if exit_code != 0:

            logger.error(f"JMeter failed with exit code {exit_code}")

            status_manager.failed()

            TestRunRepository.complete_run(
                run_id=self.test_run_id,
                status="Failed",
                end_time=datetime.now()
            )

            ExecutionManager.clear()

            return
        try:
            logger.info(
                "Starting Performance Analyzer..."
            )
            # logger.info("========== PERFORMANCE ANALYZER STARTED ==========")
            # final_time = datetime.utcnow()

            logger.info(f"Start Time : {self.start_time}")
            logger.info(f"End Time   : {final_time}")
            result = AnalyzerService().run(
                run_id=self.test_run_id,
                jtl_file=self.run.jtl_file,
                runtime_directory="reports/runtime",
                start_time=self.start_time,
                end_time=final_time
            )
            logger.info("Performance Analyzer Finished.")
            status_manager.complete()
            if result["success"]:
                TestRunRepository.complete_run(
                    run_id=self.test_run_id,
                    status="Completed",
                    end_time=datetime.now(),
                    html_report=result["html"],
                    json_report=result["json"]
                )

            ExecutionManager.clear()

            logger.info("Execution Monitor Finished Successfully.")
        except Exception:
        # status_manager.complete()
            logger.exception("Performance Analyzer failed.")
            TestRunRepository.complete_run(
                run_id=self.test_run_id,
                status="Failed",
                end_time=datetime.now()
            )
            ExecutionManager.clear()
        # logger.info("Execution Monitor Finished Successfully.")
            return


import threading


class ExecutionManager:
    _lock = threading.Lock()

    process = None
    run_id = None

    @classmethod
    def register(cls, process, run_id):

        with cls._lock:
            cls.process = process
            cls.run_id = run_id

    @classmethod
    def clear(cls):

        with cls._lock:
            cls.process = None
            cls.run_id = None

    @classmethod
    def is_running(cls):

        return cls.process is not None and cls.process.poll() is None

    @classmethod
    def stop(cls):

        with cls._lock:

            if cls.process is None:
                return False

            if cls.process.poll() is None:

                cls.process.terminate()

                try:
                    cls.process.wait(timeout=10)
                except Exception:
                    cls.process.kill()

            cls.process = None

            return True