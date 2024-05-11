import abc
from .logger import Logger, NoopLogger


class Component(metaclass=abc.ABCMeta):
    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger or NoopLogger()
