from typing import Any, Protocol

from ..models.question import MultiChoiceQuestion
from .code_to_string import default_code_as_string_factory


class MultiChoiceQuestionFactoryProtocol(Protocol):
    def __init__(
        self, code_execution_sandbox: Any, multi_choice_factory_class: Any
    ) -> None: ...
    def build(self, function: Any, choice_list: Any) -> MultiChoiceQuestion: ...


class MultiChoiceQuestionFactory(MultiChoiceQuestionFactoryProtocol):
    def __init__(self, code_execution_sandbox, multi_choice_factory_class):
        self.code_execution_sandbox = code_execution_sandbox
        self.multi_choice_factory_class = multi_choice_factory_class

    def build(self, function, choice_list):
        function_src = default_code_as_string_factory(function)
        print_logs = self.code_execution_sandbox.execute(function_src)
        question = MultiChoiceQuestion(
            correct_answer=print_logs[-1],
            function_src=function_src,
            print_logs=print_logs,
            choices=self.multi_choice_factory_class(
                print_logs[-1], choice_list
            ).build(),
        )

        return question
