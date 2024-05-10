import random

from ..models.question import InputParameterQuestion
from .code_to_string import default_code_as_string_factory


class InputParamQuestionFactory:
    def __init__(self, code_execution_sandbox):
        self.code_execution_sandbox = code_execution_sandbox

    def build(self, function, param_one):
        selected_input_param = random.choice(param_one)
        function_src = default_code_as_string_factory(function, selected_input_param)
        print_logs = self.code_execution_sandbox.execute(function_src)
        return_value = print_logs[-1]
        question = InputParameterQuestion(
            selected_param=selected_input_param,
            param_one_choices=param_one,
            function_src=function_src,
            print_logs=print_logs,
        )
        question.return_value = return_value
        return question
