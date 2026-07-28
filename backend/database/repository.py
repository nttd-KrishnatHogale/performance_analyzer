"""
database/repository.py
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from backend.database.database import Database
from backend.database.models import TestRun, ExecutionLog

from sqlalchemy import func
class TestRunRepository:


    @staticmethod
    def _get_session() -> Session:
        return Database.get_session()

    @staticmethod
    def create_test_run(
        run_name: str,
        start_time: datetime,
        status: str = "Pending"
    ) -> TestRun:

        session = Database.get_session()

        try:

            test_run = TestRun(
                # run_name=run_name,
                # start_time=start_time,
                # end_time=start_time,
                # duration=0,
                # status=status,
                # bottleneck="",
                # confidence="",
                # html_report="",
                # json_report=""
                run_name=run_name,
                status=status,
                stage="Waiting",
                progress=0,
                start_time=datetime.now()
            )

            session.add(test_run)
            session.commit()
            session.refresh(test_run)

            return test_run
        except SQLAlchemyError:

            session.rollback()

            raise

        finally:
            session.close()


    @classmethod
    def start_run(cls, run_id: int):

        session = cls._get_session()

        try:
            run = session.get(TestRun, run_id)

            if run:
                run.status = "Running"
                run.stage = "Running JMeter"
                run.progress = 10
                session.commit()

        finally:
            session.close()


    @classmethod
    def update_progress(
        cls,
        run_id: int,
        stage: str,
        progress: int,
        status: str = "Running"
    ):

        session = cls._get_session()

        try:

            run = session.get(TestRun, run_id)

            if not run:
                return
            if stage is not None:
                run.stage = stage
            if progress is not None:
                run.progress = progress
                
            run.status = status

            session.commit()

        finally:
            session.close()

    @staticmethod
    def update_test_run(
        run_id: int,
        end_time: datetime,
        duration: float,
        status: str,
        bottleneck: str = "",
        confidence: str = "",
        html_report: str = "",
        json_report: str = ""
    ) -> None:

        session = Database.get_session()

        try:

            test_run = session.get(TestRun, run_id)

            if not test_run:
                return

            test_run.end_time = end_time
            test_run.duration = duration
            test_run.status = status
            test_run.bottleneck = bottleneck
            test_run.confidence = confidence
            test_run.html_report = html_report
            test_run.json_report = json_report

            session.commit()

        finally:
            session.close()


    @classmethod
    def complete_run(
        cls,
        run_id: int,
        status: str = "Completed",
        end_time: datetime = None,
        duration: float = None,
        bottleneck: str = "",
        confidence: str = "",
        html_report: str = "",
        json_report: str = "",
        error_message: str = ""
    ):

        session = cls._get_session()

        try:

            test_run = session.get(TestRun, run_id)

            if not test_run:
                return

            if end_time is None:
                end_time = datetime.now()

            test_run.end_time = end_time

            if duration is not None:
                test_run.duration = duration
            elif test_run.start_time:
                test_run.duration = (
                    end_time - test_run.start_time
                ).total_seconds()

            test_run.status = status
            test_run.stage = "Completed"
            test_run.progress = 100

            if bottleneck:
                test_run.bottleneck = bottleneck

            if confidence:
                test_run.confidence = confidence

            if html_report:
                test_run.html_report = html_report

            if json_report:
                test_run.json_report = json_report

            if error_message:
                test_run.error_message = error_message

            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise

        finally:
            session.close()


    @classmethod
    def update_report(
        cls,
        run_id: int,
        html_report: str = "",
        json_report: str = ""
    ):
        session = cls._get_session()

        try:
            test_run = session.get(TestRun, run_id)

            if not test_run:
                return

            test_run.html_report = html_report
            test_run.json_report = json_report

            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise

        finally:
            session.close()

    @staticmethod
    def get_test_run(run_id: int) -> Optional[TestRun]:

        session = Database.get_session()

        try:
            return session.get(TestRun, run_id)

        finally:
            session.close()

    @staticmethod
    def get_all_runs() -> List[TestRun]:

        session = Database.get_session()

        try:

            return (
                session.query(TestRun)
                .order_by(desc(TestRun.id))
                .all()
            )

        finally:
            session.close()

    @staticmethod
    def delete_run(run_id: int):

        session = Database.get_session()

        try:

            test_run = session.get(TestRun, run_id)

            if test_run:

                session.delete(test_run)

                session.commit()

        finally:
            session.close()


    # --------------------------------------------------
    # Filter by Status
    # --------------------------------------------------

    @classmethod
    def get_by_status(
        cls,
        status: str
    ) -> List[TestRun]:

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .filter(TestRun.status == status)
                .order_by(TestRun.start_time.desc())
                .all()
            )

        finally:

            session.close()


    # --------------------------------------------------
    # Filter by Stage
    # --------------------------------------------------

    @classmethod
    def get_by_stage(
        cls,
        stage: str
    ) -> List[TestRun]:

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .filter(TestRun.stage == stage)
                .order_by(TestRun.id.desc())
                .all()
            )

        finally:

            session.close()

    # --------------------------------------------------
    # Date Range
    # --------------------------------------------------

    @classmethod
    def get_between_dates(
        cls,
        start_date,
        end_date
    ) -> List[TestRun]:

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .filter(
                    TestRun.start_time >= start_date,
                    TestRun.start_time <= end_date
                )
                .order_by(TestRun.start_time.desc())
                .all()
            )

        finally:

            session.close()

    # --------------------------------------------------
    # Recent Runs
    # --------------------------------------------------

    @classmethod
    def get_recent_runs(
        cls,
        limit: int = 10
    ) -> List[TestRun]:

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .order_by(TestRun.start_time.desc())
                .limit(limit)
                .all()
            )

        finally:

            session.close()

    # --------------------------------------------------
    # Pagination
    # --------------------------------------------------

    @classmethod
    def get_page(
        cls,
        page: int = 1,
        page_size: int = 20
    ):

        session = cls._get_session()

        try:

            offset = (page - 1) * page_size

            return (
                session.query(TestRun)
                .order_by(TestRun.id.desc())
                .offset(offset)
                .limit(page_size)
                .all()
            )

        finally:

            session.close()

    # --------------------------------------------------
    # Search by Run Name
    # --------------------------------------------------

    @classmethod
    def search(
        cls,
        keyword: str
    ) -> List[TestRun]:

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .filter(
                    TestRun.run_name.ilike(f"%{keyword}%")
                )
                .order_by(TestRun.id.desc())
                .all()
            )

        finally:

            session.close()

    # --------------------------------------------------
    # Latest Run
    # --------------------------------------------------

    @classmethod
    def get_latest_run(cls):

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .order_by(TestRun.id.desc())
                .first()
            )

        finally:

            session.close()
    # --------------------------------------------------
    # Running Execution
    # --------------------------------------------------

    @classmethod
    def get_running_run(cls):

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .filter(
                    TestRun.status == "Running"
                )
                .first()
            )

        finally:

            session.close()


    # --------------------------------------------------
    # Dashboard Summary
    # --------------------------------------------------

    @classmethod
    def get_dashboard_stats(cls):

        session = cls._get_session()

        try:

            total = session.query(TestRun).count()

            completed = (
                session.query(TestRun)
                .filter(TestRun.status == "Completed")
                .count()
            )

            running = (
                session.query(TestRun)
                .filter(TestRun.status == "Running")
                .count()
            )

            failed = (
                session.query(TestRun)
                .filter(TestRun.status == "Failed")
                .count()
            )

            pending = (
                session.query(TestRun)
                .filter(TestRun.status == "Pending")
                .count()
            )

            return {
                "total": total,
                "completed": completed,
                "running": running,
                "failed": failed,
                "pending": pending
            }

        finally:

            session.close()

    # --------------------------------------------------
    # Average Duration
    # --------------------------------------------------

    @classmethod
    def get_average_duration(cls):

        session = cls._get_session()

        try:

            avg = (
                session.query(
                    func.avg(TestRun.duration)
                )
                .filter(TestRun.duration > 0)
                .scalar()
            )

            return round(avg or 0, 2)

        finally:

            session.close()



    # --------------------------------------------------
    # Success Rate
    # --------------------------------------------------

    @classmethod
    def get_success_rate(cls):

        session = cls._get_session()

        try:

            total = session.query(TestRun).count()

            if total == 0:
                return 0.0

            completed = (
                session.query(TestRun)
                .filter(TestRun.status == "Completed")
                .count()
            )

            return round((completed / total) * 100, 2)

        finally:

            session.close()

    # --------------------------------------------------
    # Latest Execution
    # --------------------------------------------------

    @classmethod
    def get_latest_execution(cls):

        session = cls._get_session()

        try:

            return (
                session.query(TestRun)
                .order_by(TestRun.start_time.desc())
                .first()
            )

        finally:

            session.close()

    # --------------------------------------------------
    # Report Counts
    # --------------------------------------------------

    @classmethod
    def get_report_counts(cls):

        session = cls._get_session()

        try:

            html_reports = (
                session.query(TestRun)
                .filter(TestRun.html_report.isnot(None))
                .count()
            )

            json_reports = (
                session.query(TestRun)
                .filter(TestRun.json_report.isnot(None))
                .count()
            )

            return {
                "html_reports": html_reports,
                "json_reports": json_reports
            }

        finally:

            session.close()


    # --------------------------------------------------
    # Execution Trend
    # --------------------------------------------------

    @classmethod
    def get_execution_trend(
        cls,
        limit: int = 20
    ):

        session = cls._get_session()

        try:

            runs = (
                session.query(TestRun)
                .order_by(TestRun.start_time.desc())
                .limit(limit)
                .all()
            )

            return list(reversed(runs))

        finally:

            session.close()


    # --------------------------------------------------
    # Bottleneck Summary
    # --------------------------------------------------

    @classmethod
    def get_bottleneck_summary(cls):

        session = cls._get_session()

        try:

            rows = (
                session.query(
                    TestRun.bottleneck,
                    func.count(TestRun.id)
                )
                .filter(TestRun.bottleneck.isnot(None))
                .group_by(TestRun.bottleneck)
                .all()
            )

            return [
                {
                    "bottleneck": row[0],
                    "count": row[1]
                }
                for row in rows
            ]

        finally:

            session.close()


    # --------------------------------------------------
    # Status Distribution
    # --------------------------------------------------

    @classmethod
    def get_status_distribution(cls):

        session = cls._get_session()

        try:

            rows = (
                session.query(
                    TestRun.status,
                    func.count(TestRun.id)
                )
                .group_by(TestRun.status)
                .all()
            )

            return {
                status: count
                for status, count in rows
            }

        finally:

            session.close()




class ExecutionLogRepository:

    @staticmethod
    def add_log(
        run_id: int,
        stage: str,
        message: str
    ):

        session = Database.get_session()

        try:

            log = ExecutionLog(
                run_id=run_id,
                stage=stage,
                message=message
            )

            session.add(log)

            session.commit()

        finally:
            session.close()

    @staticmethod
    def get_logs(run_id: int):

        session = Database.get_session()

        try:

            return (
                session.query(ExecutionLog)
                .filter(
                    ExecutionLog.run_id == run_id
                )
                .all()
            )

        finally:
            session.close()

    @staticmethod
    def delete_logs(run_id: int):

        session = Database.get_session()

        try:

            logs = (
                session.query(ExecutionLog)
                .filter(
                    ExecutionLog.run_id == run_id
                )
                .all()
            )

            for log in logs:
                session.delete(log)

            session.commit()

        finally:
            session.close()