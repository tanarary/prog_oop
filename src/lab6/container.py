"""
Лабораторная работа №6 - Generics и typing
Generic-коллекция с поддержкой протоколов
"""
from typing import TypeVar, Generic, Callable, Optional, List, Protocol, Iterator
from datetime import datetime

# ============ ПРОТОКОЛЫ (для задания на 5) ============

class Displayable(Protocol):
    """Протокол для объектов, которые можно отобразить"""
    def display(self) -> str:
        """Вернуть строковое представление объекта для отображения"""
        ...

class Scorable(Protocol):
    """Протокол для объектов, которые имеют оценку/балл"""
    def score(self) -> float:
        """Вернуть числовую оценку объекта"""
        ...

# ============ TYPEVAR (с ограничениями для задания на 5) ============

T = TypeVar('T')  # Базовый TypeVar для любых типов
D = TypeVar('D', bound=Displayable)  # Только объекты с методом display()
S = TypeVar('S', bound=Scorable)     # Только объекты с методом score()
R = TypeVar('R')  # Для map-преобразований


class TypedCollection(Generic[T]):
    """
    Generic-версия коллекции пациентов.
    Может хранить объекты любого типа T.
    
    Для задания на 5 - используйте TypedCollection[D] или TypedCollection[S]
    """
    
    def __init__(self) -> None:
        """Инициализация пустой коллекции"""
        self._items: List[T] = []
    
    # ============ БАЗОВЫЕ МЕТОДЫ (из ЛР-2) ============
    
    def add(self, item: T) -> None:
        """
        Добавить элемент в коллекцию
        
        Args:
            item: элемент типа T для добавления
        """
        self._items.append(item)
        print(f"✓ Добавлен элемент в коллекцию (всего: {len(self._items)})")
    
    def remove(self, item: T) -> None:
        """
        Удалить элемент из коллекции
        
        Args:
            item: элемент для удаления
            
        Raises:
            ValueError: если элемент не найден
        """
        if item not in self._items:
            raise ValueError(f"Элемент {item} не найден в коллекции")
        self._items.remove(item)
        print(f"✓ Элемент удален из коллекции (осталось: {len(self._items)})")
    
    def get_all(self) -> List[T]:
        """
        Вернуть копию списка всех элементов
        
        Returns:
            List[T]: копия внутреннего списка
        """
        return self._items.copy()
    
    def sort_by(self, key_func: Callable[[T], any], reverse: bool = False) -> 'TypedCollection[T]':
        """
        Сортировка коллекции с использованием функции-ключа
        
        Args:
            key_func: функция, возвращающая ключ для сортировки
            reverse: сортировка в обратном порядке
        
        Returns:
            self для цепочек вызовов
        """
        self._items.sort(key=key_func, reverse=reverse)
        strategy_name = getattr(key_func, '__name__', str(key_func))
        print(f"✓ Отсортировано по: {strategy_name} (reverse={reverse})")
        return self
    
    def filter_by(self, predicate: Callable[[T], bool]) -> 'TypedCollection[T]':
        """
        Фильтрация коллекции с использованием функции-предиката
        
        Args:
            predicate: функция, возвращающая True/False для каждого элемента
        
        Returns:
            Новая коллекция с отфильтрованными элементами
        """
        new_collection = TypedCollection[T]()
        new_collection._items = list(filter(predicate, self._items))
        filter_name = getattr(predicate, '__name__', str(predicate))
        print(f"✓ Отфильтровано по: {filter_name} (осталось {len(new_collection)} элементов)")
        return new_collection
    
    def apply(self, func: Callable[[T], Optional[T]]) -> 'TypedCollection[T]':
        """
        Применить функцию ко всем элементам коллекции
        
        Args:
            func: функция для применения к каждому элементу
        
        Returns:
            self для цепочек вызовов
        """
        for i, item in enumerate(self._items):
            result = func(item)
            if result is not None and result is not item:
                self._items[i] = result
        
        func_name = getattr(func, '__name__', str(func))
        print(f"✓ Применена функция: {func_name}")
        return self
    
    def map_to(self, transform_func: Callable[[T], R]) -> List[R]:
        """
        Преобразование коллекции с помощью map()
        
        Args:
            transform_func: функция преобразования
        
        Returns:
            Список преобразованных элементов
        """
        result = list(map(transform_func, self._items))
        func_name = getattr(transform_func, '__name__', str(transform_func))
        print(f"✓ Преобразовано с помощью: {func_name}")
        return result
    
    # ============ НОВЫЕ МЕТОДЫ ДЛЯ ЗАДАНИЯ НА 4 ============
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Найти первый элемент, удовлетворяющий условию
        
        Args:
            predicate: функция-условие, возвращающая True/False
        
        Returns:
            Optional[T]: первый подходящий элемент или None
        """
        for item in self._items:
            if predicate(item):
                print(f"✓ Найден элемент по условию")
                return item
        print("✗ Элемент не найден")
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Найти все элементы, удовлетворяющие условию
        
        Args:
            predicate: функция-условие, возвращающая True/False
        
        Returns:
            List[T]: список всех подходящих элементов
        """
        result = [item for item in self._items if predicate(item)]
        print(f"✓ Отфильтровано: найдено {len(result)} элементов из {len(self._items)}")
        return result
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        """
        Преобразовать элементы коллекции с помощью функции
        
        Args:
            transform: функция преобразования
        
        Returns:
            List[R]: список преобразованных элементов (тип R может отличаться от T)
        """
        result = [transform(item) for item in self._items]
        print(f"✓ Преобразовано: {len(result)} элементов (тип изменен)")
        return result
    
    # ============ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ============
    
    def __len__(self) -> int:
        """Вернуть количество элементов"""
        return len(self._items)
    
    def __iter__(self) -> Iterator[T]:
        """Итератор по элементам коллекции"""
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        """Получить элемент по индексу"""
        return self._items[index]
    
    def __str__(self) -> str:
        """Строковое представление коллекции"""
        if not self._items:
            return "TypedCollection (пусто)"
        
        result = f"\n📋 TypedCollection ({len(self._items)} элементов):\n"
        result += "=" * 70 + "\n"
        for i, item in enumerate(self._items, 1):
            item_str = str(item)[:65] if hasattr(item, '__str__') else repr(item)
            result += f"{i:2}. {item_str}\n"
        result += "=" * 70
        return result