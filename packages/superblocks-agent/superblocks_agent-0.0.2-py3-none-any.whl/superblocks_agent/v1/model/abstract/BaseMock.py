from __future__ import annotations

from abc import ABC, abstractmethod

from type_.mock import FilteredDictCallable


class BaseMock(ABC):
    @abstractmethod
    def return_(value: dict | FilteredDictCallable) -> BaseMock:
        # TODO: doc string
        ...
