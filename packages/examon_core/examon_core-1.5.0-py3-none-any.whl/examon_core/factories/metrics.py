import ast
import logging

from ..metrics.calc_standard import CalcStandardMetrics
from ..metrics.categorize_difficulty import CategorizeDifficulty
from ..metrics.code_analysis_visitor import CodeAnalysisVisitor
from ..models.code_metrics import CodeMetrics


class CodeMetricsFactory:
    def __init__(
        self,
        calc_standard_metrics_strategy=CalcStandardMetrics,
        categorize_difficulty_strategy=CategorizeDifficulty,
    ):
        self.calc_standard_metrics_strategy = calc_standard_metrics_strategy
        self.categorize_difficulty_strategy = categorize_difficulty_strategy

    def build(self, code_as_string):
        if code_as_string == "" or code_as_string is None:
            raise Exception("Cannot use empty string")
        cm = CodeMetrics()

        standard_metrics = self.calc_standard_metrics_strategy(code_as_string).run()

        cm.difficulty = standard_metrics["difficulty"]
        cm.no_of_functions = standard_metrics["no_of_functions"]
        cm.loc = standard_metrics["loc"]
        cm.lloc = standard_metrics["lloc"]
        cm.sloc = standard_metrics["sloc"]
        cm.categorised_difficulty = self.categorize_difficulty_strategy(cm).run()

        tree = ast.parse(code_as_string)
        m = CodeAnalysisVisitor()
        m.visit(tree)

        cm.imports = list(m.modules)
        cm.calls = list(m.calls)
        cm.extra = list(m.counts)
        logging.debug(f"CodeMetricsFactory.build: {cm}")

        return cm
