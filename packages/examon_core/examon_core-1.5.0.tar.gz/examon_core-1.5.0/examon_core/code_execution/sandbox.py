class CodeExecutionSandbox:
    def __init__(self, driver_class):
        self.print_logs = None
        self.driver = driver_class()

    def execute(self, source_code):
        try:
            self.driver.setup()
            return self.driver.execute(source_code)
        finally:
            self.driver.teardown()
