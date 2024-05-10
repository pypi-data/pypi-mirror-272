from .code_execution.unrestricted_driver import UnrestrictedDriver
from .examon_in_memory_db import ExamonInMemoryDatabase
from .factories.multi_choice import MultiChoiceFactory
from .generate_unique_id import GenerateUniqueId
from .metrics.calc_standard import CalcStandardMetrics
from .metrics.categorize_difficulty import CategorizeDifficulty


class ExamonGlobalSettings:
    # Global properties
    record_metrics = True
    repository = None
    version = None

    # QuestionFactory
    code_execution_driver_class = UnrestrictedDriver
    multi_choice_factory_class = MultiChoiceFactory
    calc_standard_metrics_strategy = CalcStandardMetrics
    categorize_difficulty_strategy = CategorizeDifficulty
    unique_id_strategy = GenerateUniqueId

    # Save the items
    in_memory_db = ExamonInMemoryDatabase
