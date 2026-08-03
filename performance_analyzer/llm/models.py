from dataclasses import dataclass


@dataclass
class RCAReport:

    summary: str

    root_cause: str

    timeline: str

    bottlenecks: list

    recommendations: list

    confidence: str