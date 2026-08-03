from dataclasses import dataclass


@dataclass
class ApacheFinding:

    finding: str

    severity: str

    score: int

    description: str

    recommendation: str

    evidence: dict