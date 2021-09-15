from dataclasses import dataclass

@dataclass
class Error:
    reason: str
    code: int