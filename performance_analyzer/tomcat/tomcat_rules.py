from dataclasses import dataclass

@dataclass
class TomcatFinding:

    finding: str

    severity: str

    score: int

    description: str

    recommendation: str

    evidence: dict