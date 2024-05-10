import logging
from typing import Protocol, Any


class MultiChoiceProtocol(Protocol):
    def __init__(self, code_execution_sandbox: Any) -> None: ...
    def build(self, function: Any, choice_list: Any) -> Any: ...


class MultiChoiceFactory(MultiChoiceProtocol):
    def __init__(self, correct_answer, choice_list=None, src_code=None):
        self.correct_answer = correct_answer
        self.choice_list = choice_list

    def build(self):
        if self.correct_answer not in self.choice_list:
            logging.debug(
                f"MultiChoiceFactory.build: {self.correct_answer} not in {self.choice_list}"
            )
            self.choice_list.append(self.correct_answer)

        logging.debug(f"MultiChoiceFactory.build: {self.choice_list}")
        return self.choice_list
