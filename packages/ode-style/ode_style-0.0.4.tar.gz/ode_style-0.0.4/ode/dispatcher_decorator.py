from abc import abstractmethod
from typing import TypeVar, Optional
from ode.use_case import UseCase
from ode.output import Output
from ode.use_case_decorator import UseCaseDecorator
import asyncio

P = TypeVar('P')
R = TypeVar('R')

class DispatcherDecorator(UseCaseDecorator[P, R]):
    def __init__(
        self,
        use_case: UseCase[P, R],
        execute_on: asyncio.AbstractEventLoop = None,
        result_on: asyncio.AbstractEventLoop = None
    ):
        super().__init__(use_case)
        self.execute_on = execute_on
        self.result_on = result_on

    def dispatch(self, param: Optional[P] = None):
        return asyncio.create_task(self.process(param), loop=self.execute_on)

    def on_error(self, error: Exception):
        asyncio.to_thread(self.use_case.on_error, error, loop=self.result_on)

    def on_result(self, output: Output[R]):
        asyncio.to_thread(self.use_case.on_result, output, loop=self.result_on)