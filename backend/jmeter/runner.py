"""
backend/jmeter/runner.py

JMeter execution service.
"""

from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from click import command

from config.config_service import ConfigService
from backend.utils.logger import Logger


# ==========================================================
# Result Object
# ==========================================================

@dataclass
class JMeterResult:
    """
    Result returned after a JMeter execution.
    """

    success: bool = False

    exit_code: int = -1

    status: str = "NOT_STARTED"

    start_time: Optional[datetime] = None

    end_time: Optional[datetime] = None

    duration_seconds: float = 0.0

    stdout: str = ""

    stderr: str = ""

    jtl_file: Optional[str] = None

    log_file: Optional[str] = None

    csv_file: Optional[str] = None

    error_message: Optional[str] = None

    command: List[str] = field(default_factory=list)


# ==========================================================
# JMeter Runner
# ==========================================================

class JMeterRunner:

    def __init__(self):

        self.logger = Logger.get_logger()

        self.config = ConfigService()

        self._load_configuration()

    # ------------------------------------------------------

    def _load_configuration(self):

        """
        Read configuration from config.yaml.
        """

        self.jmeter_home = self.config.get("jmeter.home")

        self.jmeter_executable = self.config.get(
            "jmeter.executable"
        )

        self.test_plan = self.config.get(
            "jmeter.test_plan"
        )

        self.results_directory = self.config.get(
            "jmeter.results_directory"
        )

        self.jvm_args = self.config.get(
            "jmeter.jvm_args",
            ""
        )

        Path(self.results_directory).mkdir(
            parents=True,
            exist_ok=True
        )

        if self.jmeter_executable is None:

            raise ValueError(
                "JMeter executable not configured."
            )

        self.logger.info(
            "JMeter configuration loaded successfully."
        )

    # ------------------------------------------------------

    def build_command(
        self,
        run_name: Optional[str] = None
    ) -> Dict[str, object]:

        """
        Build JMeter command.

        Returns:

            {
                "command": [...],
                "jtl": "...",
                "csv": "...",
                "log": "..."
            }
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        if run_name:

            base_name = f"{run_name}_{timestamp}"

        else:

            base_name = timestamp

        jtl_file = os.path.join(
            self.results_directory,
            f"{base_name}.jtl"
        )

        csv_file = os.path.join(
            self.results_directory,
            f"{base_name}.csv"
        )

        log_file = os.path.join(
            self.results_directory,
            f"{base_name}.log"
        )

        executable = self.jmeter_executable

        if (
            platform.system() == "Windows"
            and executable.lower().endswith(".bat") is False
        ):
            executable += ".bat"

        command = [

            executable,

            "-n",

            "-t",
            self.test_plan,

            "-l",
            jtl_file,

            "-j",
            log_file,

            "-e",

            "-o",
            os.path.join(
                self.results_directory,
                f"{base_name}_dashboard"
            ),
        ]

        if self.jvm_args:

            command.extend(
                [
                    "-Jjmeterengine.force.system.exit=true",
                    f"-J{self.jvm_args}"
                ]
            )

        self.logger.info(
            "JMeter command created successfully."
        )

        return {

            "command": command,

            "jtl": jtl_file,

            "csv": csv_file,

            "log": log_file,

            "dashboard": os.path.join(
                self.results_directory,
                f"{base_name}_dashboard"
            ),
        }

    # ------------------------------------------------------

    def validate(self):

        """
        Validate JMeter configuration before execution.
        """

        if not os.path.exists(self.jmeter_executable):

            raise FileNotFoundError(
                f"JMeter executable not found: "
                f"{self.jmeter_executable}"
            )

        if not os.path.exists(self.test_plan):

            raise FileNotFoundError(
                f"Test Plan not found: "
                f"{self.test_plan}"
            )

        self.logger.info(
            "JMeter validation successful."
        )



    def start_process(
        self,
        run_name: Optional[str] = None
    ):

        self.validate()

        build = self.build_command(run_name)

        result = JMeterResult()

        result.command = build["command"]
        result.jtl_file = build["jtl"]
        result.csv_file = build["csv"]
        result.log_file = build["log"]

        result.start_time = datetime.now()
        result.status = "RUNNING"

        self.logger.info("Starting JMeter...")

        process = subprocess.Popen(
            build["command"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        self.logger.info("JMeter Started Successfully")
        self.logger.info(f"PID : {process.pid}")
        self.logger.info("===== COMMAND =====")
        self.logger.info(
    f"Command : {' '.join(build['command'])}"
)
        return process, result

            # ------------------------------------------------------
    # Execute JMeter
    # ------------------------------------------------------

    def execute(
        self,
        run_name: Optional[str] = None,
        timeout: int = 3600
    ) -> JMeterResult:

        self.validate()

        build = self.build_command(run_name)

        result = JMeterResult()

        result.command = build["command"]
        result.jtl_file = build["jtl"]
        result.csv_file = build["csv"]
        result.log_file = build["log"]

        result.start_time = datetime.now()
        result.status = "RUNNING"

        self.logger.info(
            "Starting JMeter execution..."
        )
        self.logger.info(
            " ".join(build["command"])
        )

    
        try:

            process = subprocess.Popen(
                build["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )

            stdout, stderr = process.communicate(
                timeout=timeout
            )
            if stdout:

                self.logger.info("===== JMeter Output =====")
                self.logger.info(stdout)

            if stderr:

                self.logger.error("===== JMeter Error =====")
                self.logger.error(stderr)
            result.exit_code = process.returncode

            result.stdout = stdout or ""
            result.stderr = stderr or ""

            result.end_time = datetime.now()

            result.duration_seconds = (
                result.end_time -
                result.start_time
            ).total_seconds()
            self.logger.info(f"PID : {process.pid}")

            return self._process_result(result)

        except subprocess.TimeoutExpired:

            self.logger.error(
                "JMeter execution timed out."
            )

            process.kill()

            stdout, stderr = process.communicate()

            result.stdout = stdout or ""
            result.stderr = stderr or ""

            result.status = "TIMEOUT"

            result.success = False

            result.error_message = (
                f"Execution exceeded "
                f"{timeout} seconds."
            )

            result.end_time = datetime.now()

            result.duration_seconds = (
                result.end_time -
                result.start_time
            ).total_seconds()

            return result

        except Exception as ex:

            self.logger.exception(ex)

            result.success = False

            result.status = "FAILED"

            result.error_message = str(ex)

            result.end_time = datetime.now()

            result.duration_seconds = (
                result.end_time -
                result.start_time
            ).total_seconds()

            return result

    # ------------------------------------------------------
    # Process Result
    # ------------------------------------------------------


    def finish_process(
        self,
        process,
        result: JMeterResult
    ):

        stdout, stderr = process.communicate()

        result.stdout = stdout or ""
        result.stderr = stderr or ""

        result.exit_code = process.returncode

        result.end_time = datetime.now()

        result.duration_seconds = (
            result.end_time -
            result.start_time
        ).total_seconds()

        return self._process_result(result)

    def _process_result(
        self,
        result: JMeterResult
    ) -> JMeterResult:

        if result.exit_code != 0:

            result.success = False

            result.status = "FAILED"

            result.error_message = (
                f"JMeter exited with "
                f"code {result.exit_code}"
            )

            self.logger.error(
                result.error_message
            )

            return result

        if result.stderr.strip():

            self.logger.warning(
                "JMeter produced stderr output."
            )

        if not os.path.exists(result.jtl_file):

            result.success = False

            result.status = "FAILED"

            result.error_message = (
                "JTL result file not generated."
            )

            self.logger.error(
                result.error_message
            )

            return result

        if os.path.getsize(result.jtl_file) == 0:

            result.success = False

            result.status = "FAILED"

            result.error_message = (
                "Generated JTL file is empty."
            )

            self.logger.error(
                result.error_message
            )

            return result

        result.success = True

        result.status = "COMPLETED"

        self.logger.info(
            f"Execution completed in "
            f"{result.duration_seconds:.2f} seconds."
        )

        self.logger.info(
            f"Result File : {result.jtl_file}"
        )

        self.logger.info(
            f"Log File : {result.log_file}"
        )

        return result
    
        # ------------------------------------------------------
    # Result Parsing
    # ------------------------------------------------------

    def parse_result(
        self,
        result: JMeterResult
    ) -> dict:
        """
        Build a lightweight summary after execution.
        Detailed metrics will be extracted later by the
        CSV parser.
        """

        summary = {

            "success": result.success,

            "status": result.status,

            "exit_code": result.exit_code,

            "duration": result.duration_seconds,

            "start_time": result.start_time,

            "end_time": result.end_time,

            "jtl_file": result.jtl_file,

            "csv_file": result.csv_file,

            "log_file": result.log_file,

            "stdout_length": len(result.stdout),

            "stderr_length": len(result.stderr),

            "error_message": result.error_message

        }

        return summary

    # ------------------------------------------------------
    # Retry Execution
    # ------------------------------------------------------

    def execute_with_retry(
        self,
        run_name: str,
        retries: int = 2,
        timeout: int = 3600
    ) -> JMeterResult:

        last_result = None

        for attempt in range(1, retries + 2):

            self.logger.info(
                f"Execution Attempt {attempt}"
            )

            last_result = self.execute(
                run_name=run_name,
                timeout=timeout
            )

            if last_result.success:

                return last_result

            self.logger.warning(
                "Execution failed."
            )

        return last_result

    # ------------------------------------------------------
    # Verify Dashboard
    # ------------------------------------------------------

    def dashboard_exists(
        self,
        dashboard_path: str
    ) -> bool:

        index = os.path.join(
            dashboard_path,
            "index.html"
        )

        return os.path.exists(index)

    # ------------------------------------------------------
    # Verify Result File
    # ------------------------------------------------------

    def result_exists(
        self,
        result: JMeterResult
    ) -> bool:

        return (
            result.jtl_file is not None
            and
            os.path.exists(result.jtl_file)
        )

    # ------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------

    def cleanup(
        self,
        result: JMeterResult,
        remove_log=False
    ):

        if remove_log:

            if (
                result.log_file
                and
                os.path.exists(result.log_file)
            ):

                os.remove(result.log_file)

    # ------------------------------------------------------
    # Return Dictionary
    # ------------------------------------------------------

    def to_dict(
        self,
        result: JMeterResult
    ) -> dict:

        return {

            "success": result.success,

            "status": result.status,

            "exit_code": result.exit_code,

            "duration": result.duration_seconds,

            "stdout": result.stdout,

            "stderr": result.stderr,

            "jtl_file": result.jtl_file,

            "csv_file": result.csv_file,

            "log_file": result.log_file,

            "error_message": result.error_message

        }