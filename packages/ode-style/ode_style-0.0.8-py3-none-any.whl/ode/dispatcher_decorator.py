import threading
import queue
from ode.use_case_decorator import UseCaseDecorator

class UseCaseDispatcher:
    def __init__(self, use_case, execute_on=queue.Queue()):
        self.decorator = DispatcherDecorator(use_case, execute_on)

    def dispatch(self, param=None):
        return self.decorator.dispatch(param)

class DispatcherDecorator(UseCaseDecorator):
    def __init__(self, use_case, result_on: queue.Queue):
        super().__init__(use_case)
        self.result_on = result_on

    def dispatch(self, param=None):
        threading.Thread(target=self.process(param=param), daemon=True).start()

    def on_error(self, error):
        threading.Thread(target=self.result_on.task_done(error), daemon=True).start()
        self.result_on.join()

    def on_result(self, output):
        threading.Thread(target=self.result_on.task_done(output), daemon=True).start()
        self.result_on.join()