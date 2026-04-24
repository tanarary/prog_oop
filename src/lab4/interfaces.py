
from abc import ABC, abstractmethod
from typing import Any


class Printable(ABC):
    """
    Интерфейс для объектов, которые могут предоставить строковое представление
    в разных форматах для разных целей
    """
    
    @abstractmethod
    def to_string(self, format_type: str = "default") -> str:
        pass
    
    @abstractmethod
    def to_short_string(self) -> str:
        pass


class Comparable(ABC):
    """
    Интерфейс для объектов, которые можно сравнивать между собой
    Реализует контракт сравнения, аналогичный Java Comparable
    """
    
    @abstractmethod
    def compare_to(self, other: Any) -> int:
        pass
    
    @abstractmethod
    def get_sort_key(self) -> Any:
        pass