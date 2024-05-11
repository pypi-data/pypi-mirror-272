from ode.error_output import ErrorOutput
from ode.use_case import UseCase
from ode.output import Output
from ode.use_case_decorator import UseCaseDecorator
from typing import Callable, TypeVar

P = TypeVar('P')
R = TypeVar('R')

class CallbackDecorator(UseCaseDecorator[P, R]):
    
    def __init__(self, use_case: UseCase[P, R], callback: Callable[[Output[R]], None]):
        super().__init__(use_case)
        self.callback = callback

    def task_done(self, output: Output[R]):
        if(output.is_success):
            self.callback(output)
            return
        
        self.callback(ErrorOutput(output.error))