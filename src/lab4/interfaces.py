
from abc import ABC, abstractmethod
from typing import Any


class Printable(ABC):
    """
    Интерфейс для объектов, которые могут предоставить строковое представление
    в разных форматах для разных целей
    """
    
    @abstractmethod
    def to_string(self, format_type: str = "default") -> str:
        """
        Получить строковое представление объекта
        Args:
            format_type: тип форматирования ("default", "short", "detailed")
        Returns:
            отформатированная строка
        """
        pass
    
    @abstractmethod
    def to_short_string(self) -> str:
        """Краткое представление (например, для списков)"""
        pass


class Comparable(ABC):
    """
    Интерфейс для объектов, которые можно сравнивать между собой
    Реализует контракт сравнения, аналогичный Java Comparable
    """
    
    @abstractmethod
    def compare_to(self, other: Any) -> int:
        """
        Сравнить текущий объект с другим
        Args:
            other: объект для сравнения
        Returns:
            -1 если self < other
            0 если self == other
            1 если self > other
        Raises:
            TypeError: если other не поддерживает сравнение
        """
        pass
    
    @abstractmethod
    def get_sort_key(self) -> Any:
        """
        Получить ключ для сортировки (альтернативный подход)
        Returns:
            значение, по которому можно сортировать (число, строка, дата)
        """
        pass