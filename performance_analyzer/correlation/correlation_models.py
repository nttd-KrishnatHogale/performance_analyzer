from dataclasses import dataclass


@dataclass
class Correlation:

    source: str

    target: str

    relation: str

    confidence: float

    evidence: list