"""
ЛР-5: Расширение коллекции PatientRegistry
Добавлены методы для функционального стиля
"""

from typing import List, Optional, Callable, Union, Iterator
from base import Patient
import strategies


class PatientRegistry:
    """
    Коллекция для хранения пациентов с поддержкой функций высшего порядка
    """
    
    def __init__(self):
        """Инициализация пустой коллекции"""
        self._items: List[Patient] = []
    
    # ============ БАЗОВЫЕ МЕТОДЫ (из ЛР-2) ============
    
    def add(self, patient: Patient) -> None:
        """Добавить пациента в коллекцию"""
        if not isinstance(patient, Patient):
            raise TypeError(f"Можно добавлять только объекты Patient")
        
        if self._find_by_id(patient.patient_id) is not None:
            raise ValueError(f"Пациент с ID {patient.patient_id} уже существует")
        
        self._items.append(patient)
        print(f"✓ Пациент '{patient.full_name}' добавлен в реестр")
    
    def remove(self, patient: Patient) -> None:
        """Удалить пациента из коллекции"""
        if patient not in self._items:
            raise ValueError(f"Пациент не найден")
        self._items.remove(patient)
    
    def get_all(self) -> List[Patient]:
        """Вернуть копию списка всех пациентов"""
        return self._items.copy()
    
    def _find_by_id(self, patient_id: int) -> Optional[Patient]:
        for patient in self._items:
            if patient.patient_id == patient_id:
                return patient
        return None
    
    # ============ НОВЫЕ МЕТОДЫ ДЛЯ ЛР-5 ============
    
    def sort_by(self, key_func: Callable, reverse: bool = False) -> 'PatientRegistry':
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
    
    def filter_by(self, predicate: Callable) -> 'PatientRegistry':
        """
        Фильтрация коллекции с использованием функции-предиката
        
        Args:
            predicate: функция, возвращающая True/False для каждого элемента
        
        Returns:
            Новая коллекция с отфильтрованными элементами
        """
        new_registry = PatientRegistry()
        new_registry._items = list(filter(predicate, self._items))
        filter_name = getattr(predicate, '__name__', str(predicate))
        print(f"✓ Отфильтровано по: {filter_name} (осталось {len(new_registry)} пациентов)")
        return new_registry
    
    def apply(self, func: Callable) -> 'PatientRegistry':
        """
        Применить функцию ко всем элементам коллекции
        
        Args:
            func: функция для применения к каждому пациенту
        
        Returns:
            self для цепочек вызовов
        """
        for i, patient in enumerate(self._items):
            result = func(patient)
            # Если функция возвращает измененного пациента, обновляем элемент
            if isinstance(result, Patient) and result is not patient:
                self._items[i] = result
        
        func_name = getattr(func, '__name__', str(func))
        print(f"✓ Применена функция: {func_name}")
        return self
    
    def map_to(self, transform_func: Callable) -> List:
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
    
    def chain(self) -> 'PatientRegistryChain':
        """
        Начать цепочку операций
        
        Returns:
            Объект для построения цепочки
        """
        return PatientRegistryChain(self)
    
    # ============ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ============
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self) -> Iterator[Patient]:
        return iter(self._items)
    
    def __getitem__(self, index) -> Patient:
        return self._items[index]
    
    def __str__(self) -> str:
        if not self._items:
            return "PatientRegistry (пусто)"
        
        result = f"\n📋 PatientRegistry ({len(self._items)} пациентов):\n"
        result += "=" * 70 + "\n"
        for i, patient in enumerate(self._items, 1):
            result += f"{i:2}. {str(patient)[:65]}\n"
        result += "=" * 70
        return result


class PatientRegistryChain:
    """
    Класс для построения цепочек операций (Builder pattern)
    """
    
    def __init__(self, registry: PatientRegistry):
        self._registry = registry
        self._current = registry
    
    def filter(self, predicate: Callable) -> 'PatientRegistryChain':
        """Добавить фильтрацию в цепочку"""
        self._current = self._current.filter_by(predicate)
        return self
    
    def sort(self, key_func: Callable, reverse: bool = False) -> 'PatientRegistryChain':
        """Добавить сортировку в цепочку"""
        self._current.sort_by(key_func, reverse)
        return self
    
    def apply(self, func: Callable) -> 'PatientRegistryChain':
        """Добавить apply в цепочку"""
        self._current.apply(func)
        return self
    
    def result(self) -> PatientRegistry:
        """Получить результат цепочки"""
        return self._current