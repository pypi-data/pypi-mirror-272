import inspect
import logging


class CodeAsStringFactory:
    def __init__(self, decorators=None):
        self.decorators = [] if decorators is None else decorators

    def build(self, function):
        src_code = CodeAsStringFactory.function_src(function)
        for decorator in self.decorators:
            logging.debug(f"CodeAsStringFactory.build: {decorator}")
            src_code = decorator.decorate(src_code)
            logging.debug(f"CodeAsStringFactory.build: {src_code}")

        logging.debug(f"CodeAsStringFactory.build: {src_code}")
        return src_code

    @staticmethod
    def function_src(function):
        logging.debug(f"CodeAsStringFactory.function_src: {function}")
        return inspect.getsource(function).strip()


class SourceCodeCommentsDecorator:
    def __init__(self, hints):
        self.hints = hints

    def decorate(self, src_code):
        all_hints = ""
        if self.hints is None:
            return all_hints
        else:
            for hint in self.hints:
                all_hints += f"# {hint}\n"
        all_hints = f"# Hints:\n{all_hints}\n\n"
        return all_hints + src_code


class RemoveQuizItemDecorator:
    def decorate(self, src_code):
        return src_code[src_code.find("def") :]


class AppendPrintDecorator:
    def __init__(self, function_name, param=""):
        self.function_name = function_name
        self.param = param

    def decorate(self, src_code):
        if isinstance(self.param, str) and self.param != "":
            self.param = f"'{self.param}'"
        println = f"\n\nprint({self.function_name}({self.param}))"
        return src_code + println


def default_code_as_string_factory(function, param=""):
    return CodeAsStringFactory(
        [RemoveQuizItemDecorator(), AppendPrintDecorator(function.__name__, param)]
    ).build(function)
