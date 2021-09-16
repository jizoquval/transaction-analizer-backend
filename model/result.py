from dataclasses import dataclass

@dataclass
class Result:
    id: str
    predicted_sum: int
    real_sum: int
    category: str
    month: int
