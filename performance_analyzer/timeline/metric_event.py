from dataclasses import dataclass

@dataclass
class MetricEvent:

    metric:str

    hostname:str

    layer:str

    start_time=None

    peak_time=None

    end_time=None

    start_value=None

    peak_value=None

    end_value=None

    duration=None

    severity="LOW"

    confidence=0

    description=""