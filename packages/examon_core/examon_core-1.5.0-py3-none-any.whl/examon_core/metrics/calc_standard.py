from typing import Dict, Protocol

from radon.metrics import h_visit
from radon.raw import analyze


class CalcStandardMetricsProtocol(Protocol):
    def __init__(self, code_as_string: str) -> None: ...
    def run(self) -> Dict[str, float]: ...


class CalcStandardMetrics(CalcStandardMetricsProtocol):
    def __init__(self, code_as_string):
        self.code_as_string = code_as_string

    def run(self):
        raw = analyze(self.code_as_string)
        visit_data = h_visit(self.code_as_string)
        return {
            "difficulty": round(visit_data.total.difficulty, 2),
            "no_of_functions": len(visit_data.functions),
            "loc": raw.loc,
            "lloc": raw.lloc,
            "sloc": raw.sloc,
        }
