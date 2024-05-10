from ..models.question import BaseQuestion
from .code_to_string import default_code_as_string_factory


class BaseQuestionFactory:

    def __init__(self, code_execution_sandbox):
        self.code_execution_sandbox = code_execution_sandbox

    def build(self, function):
        function_src = default_code_as_string_factory(function)
        print_logs = self.code_execution_sandbox.execute(function_src)
        question = BaseQuestion(
            function_src=function_src,
            print_logs=print_logs,
            correct_answer=print_logs[-1],
        )
        return question
