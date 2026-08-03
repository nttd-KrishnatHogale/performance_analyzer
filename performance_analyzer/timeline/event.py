from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TimelineEvent:

    component: str

    metric: str

    severity: str

    description: str

    threshold: float

    peak_value: float

    start_time: datetime

    peak_time: datetime

    recovery_time: Optional[datetime]

    duration_seconds: float = 0

    confidence: float = 1.0

    metadata: dict = None