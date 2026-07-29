"""
status_manager.py

Tracks execution status of the Performance Engineering Platform.
"""

from datetime import datetime
from threading import Lock


class StatusManager:

    _instance = None
    _lock = Lock()

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.reset()

        return cls._instance

    def reset(self):

        self.run_id = None

        self.status = "Idle"

        self.stage = "Waiting"

        self.progress = 0

        self.message = ""

        self.start_time = None

        self.end_time = None

        self.error = None

    def start(self, run_id):

        self.run_id = run_id

        self.status = "Running"

        self.stage = "Initializing"

        self.progress = 0

        self.start_time = datetime.now()

        self.message = "Execution Started"

        self.error = None

    def update(self,
    stage=None,
    progress=None,
    message=None,
    status=None):


        if stage is not None:
            self.stage = stage

        if progress is not None:
            self.progress = progress

        if message is not None:
            self.message = message

        if status is not None:
            self.status = status

    def complete(self):

        self.status = "Completed"

        self.progress = 100

        self.stage = "Completed"

        self.end_time = datetime.now()

        self.message = "Performance Test Completed"

    def failed(self, error):

        self.status = "Failed"

        self.stage = "Failed"

        self.error = str(error)

        self.end_time = datetime.now()

        self.message = str(error)

    def get_status(self):

        return {

            "run_id": self.run_id,

            "status": self.status,

            "stage": self.stage,

            "progress": self.progress,

            "message": self.message,

            "start_time": self.start_time,

            "end_time": self.end_time,

            "error": self.error

        }


status_manager = StatusManager()