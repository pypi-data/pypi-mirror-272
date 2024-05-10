import logging
from typing import Any, List, Protocol

from examon_core.code_execution.unrestricted_driver import DriverProtocol
from examon_core.factories.multi_choice import MultiChoiceProtocol
from examon_core.generate_unique_id import GenerateUniqueIdProtocol
from examon_core.metrics.calc_standard import CalcStandardMetricsProtocol
from examon_core.metrics.categorize_difficulty import CategorizeDifficultyProtocol

from ..code_execution.sandbox import CodeExecutionSandbox
from ..global_settings import ExamonGlobalSettings
from .base_question import BaseQuestionFactory
from .input_param_question import InputParamQuestionFactory
from .metrics import CodeMetricsFactory
from .multi_choice_question import MultiChoiceQuestionFactory


class InvalidAnswerException(Exception):
    pass


class ItemFactoryProtocol(Protocol):
    def build(
        self,
        function=None,
        tags=None,
        internal_id=None,
        hints=None,
        param1=None,
        choices=None,
        choice_list=None,
        repository=None,
        version=None,
        metrics=None,
    ) -> Any:
        pass

    def choice_list_as_string(self, choices) -> List[str]:
        pass


class ItemFactory(ItemFactoryProtocol):
    def __init__(
        self,
        code_execution_driver_class: DriverProtocol = None,
        multi_choice_factory_class: MultiChoiceProtocol = None,
        calc_standard_metrics_class: CalcStandardMetricsProtocol = None,
        categorize_difficulty_class: CategorizeDifficultyProtocol = None,
        unique_id_strategy: GenerateUniqueIdProtocol = None,
    ) -> None:
        self.code_execution_driver_class = code_execution_driver_class
        self.multi_chioce_factory_class = multi_choice_factory_class
        self.calc_standard_metrics_strategy = calc_standard_metrics_class
        self.categorize_difficulty_strategy = categorize_difficulty_class
        self.unique_id_strategy = unique_id_strategy

    def build(
        self,
        function=None,
        tags=None,
        internal_id=None,
        hints=None,
        param1=None,
        choices=None,
        choice_list=None,
        repository=None,
        version=None,
        metrics=None,
    ):

        result_choice_list = self.choice_list_as_string(choices or choice_list)
        ces = CodeExecutionSandbox(self.code_execution_driver_class)

        # Build
        if param1 is not None:
            question = InputParamQuestionFactory(ces).build(function, param1)
        elif result_choice_list:
            question = MultiChoiceQuestionFactory(
                code_execution_sandbox=ces,
                multi_choice_factory_class=self.multi_chioce_factory_class,
            ).build(function, result_choice_list)
        else:
            question = BaseQuestionFactory(ces).build(function)

        if metrics:
            question.metrics = CodeMetricsFactory(
                calc_standard_metrics_strategy=self.calc_standard_metrics_strategy,
                categorize_difficulty_strategy=self.categorize_difficulty_strategy,
            ).build(question.function_src)

        question.hints = hints
        question.internal_id = internal_id
        question.tags = tags
        question.repository = repository
        question.version = version

        question.unique_id = self.unique_id_strategy().run(question.function_src)
        logging.debug(f"QuestionFactory.build: {question}")
        return question

    def choice_list_as_string(self, choices):
        result_choice_list = []
        if choices:
            result_choice_list = list(map(lambda x: str(x), choices))
        return result_choice_list

    @staticmethod
    def default_instance(
        code_execution_driver_class=None,
        multi_chioce_factory_class=None,
        calc_standard_metrics_strategy=None,
        categorize_difficulty_strategy=None,
        unique_id_strategy=None,
    ):
        return ItemFactory(
            code_execution_driver_class=code_execution_driver_class
            or ExamonGlobalSettings.code_execution_driver_class,
            multi_choice_factory_class=multi_chioce_factory_class
            or ExamonGlobalSettings.multi_choice_factory_class,
            calc_standard_metrics_class=calc_standard_metrics_strategy
            or ExamonGlobalSettings.calc_standard_metrics_strategy,
            categorize_difficulty_class=categorize_difficulty_strategy
            or ExamonGlobalSettings.categorize_difficulty_strategy,
            unique_id_strategy=unique_id_strategy
            or ExamonGlobalSettings.unique_id_strategy,
        )
