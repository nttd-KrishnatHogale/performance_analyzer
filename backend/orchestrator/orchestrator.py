from threading import Thread
from datetime import datetime

from backend.jmeter.runner import JMeterRunner
from backend.monitoring.execution_monitor import ExecutionMonitor
from backend.database.repository import TestRunRepository
from backend.orchestrator.status_manager import status_manager
from backend.utils.logger import Logger


logger = Logger.get_logger()


class TestOrchestrator:

    def __init__(self):
        self.runner = JMeterRunner()

    def start_test(self):

        logger.info("Creating Test Run")

        run = TestRunRepository.create_test_run(
            run_name=f"LoadTest_{datetime.now():%Y%m%d_%H%M%S}",
            start_time=datetime.now(),
        )
        run_id = run.id
        status_manager.start(run_id)

        logger.info("Launching JMeter")
        try:

            process, result = self.runner.start_process(
                run_name=run.run_name
            )
        except Exception as ex:
            logger.exception(ex)


            status_manager.failed(str(ex))

            TestRunRepository.complete_run(
                run_id=run.id,
                end_time=datetime.now(),
                status="FAILED"
            )

            raise


        from backend.monitoring.execution_monitor import ExecutionManager

        ExecutionManager.register(
            process,
            run_id
        )

        monitor = ExecutionMonitor(
                process=process,
                run=result,
                test_run_id=run.id,
                start_time=result.start_time
            )

        thread = Thread(
                target=monitor.monitor,
                daemon=True
            )

        thread.start()

        logger.info("Background Monitor Started")

        return run.id