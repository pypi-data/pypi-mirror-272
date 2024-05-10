from abc import abstractmethod
from typing import TypeVar, Optional
from ode.dispatcher_decorator import DispatcherDecorator
from ode.use_case import UseCase
import asyncio

P = TypeVar('P')
R = TypeVar('R')

class UseCaseDispatcher:
    def __init__(
        self,
        use_case: UseCase[P, R],
        execute_on: asyncio.AbstractEventLoop = None,
        result_on: asyncio.AbstractEventLoop = None
    ):
        self.decorator = DispatcherDecorator(use_case, execute_on, result_on)

    def dispatch(self, param: Optional[P] = None):
        return self.decorator.dispatch(param)