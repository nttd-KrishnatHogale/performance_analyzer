from dataclasses import dataclass


@dataclass
class OracleFinding:

    finding: str

    severity: str

    score: int

    description: str

    recommendation: str

    evidence: dict