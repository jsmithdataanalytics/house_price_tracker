from abc import ABC, abstractmethod
from typing import Iterable


class PropertyLister(ABC):

    @abstractmethod
    def get_listings(self) -> Iterable:
        pass
