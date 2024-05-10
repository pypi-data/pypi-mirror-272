from typing import Any, Protocol


class CategorizeDifficultyProtocol(Protocol):
    def __init__(self, code_as_string: Any) -> None: ...
    def run(self) -> str: ...


class CategorizeDifficulty(CategorizeDifficultyProtocol):
    def __init__(self, metrics):
        self.metrics = metrics

    def run(self):
        value = self.metrics.difficulty
        if value == 0:
            return "Easy"
        elif 0 < value <= 1:
            return "Medium"
        elif 1 < value < 3:
            return "Hard"
        elif value >= 3:
            return "Very Hard"
