

import sys
import os

# Добавляем корень проекта в путь (если запускаете не через -m)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Optional, Callable, Iterator
from lab3.models import Patient
import lab5.strategies as st


class PatientRegistry:
    """
    Коллекция для хранения пациентов с поддержкой функций высшего порядка
    """
    
    def __init__(self):
        self._items: List[Patient] = []
    
    # ---------- Базовые методы ----------
    def add(self, patient: Patient) -> None:
        if not isinstance(patient, Patient):
            raise TypeError("Можно добавлять только объекты Patient")
        if self._find_by_id(patient.patient_id) is not None:
            raise ValueError(f"Пациент с ID {patient.patient_id} уже существует")
        self._items.append(patient)
        print(f"✓ Пациент '{patient.full_name}' добавлен в реестр")
    
    def remove(self, patient: Patient) -> None:
        if patient not in self._items:
            raise ValueError(f"Пациент не найден")
        self._items.remove(patient)
    
    def get_all(self) -> List[Patient]:
        return self._items.copy()
    
    def _find_by_id(self, patient_id: int) -> Optional[Patient]:
        for patient in self._items:
            if patient.patient_id == patient_id:
                return patient
        return None
    
    # ---------- Методы поиска ----------
    def find_by_id(self, patient_id: int) -> Optional[Patient]:
        """Публичный поиск по ID"""
        return self._find_by_id(patient_id)
    
    def find_by_name(self, substring: str) -> List[Patient]:
        """Поиск по части ФИО (без учёта регистра)"""
        substring = substring.lower()
        return [p for p in self._items if substring in p.full_name.lower()]
    
    def find_by_diagnosis(self, substring: str) -> List[Patient]:
        """Поиск по части диагноза"""
        substring = substring.lower()
        return [p for p in self._items if substring in p.diagnosis.lower()]
    
    def find_by_status(self, status: str) -> List[Patient]:
        """Поиск по статусу"""
        return [p for p in self._items if p.status == status]
    
    # ---------- Сортировка ----------
    def sort_by(self, key_func: Callable, reverse: bool = False) -> 'PatientRegistry':
        """Сортировка коллекции с использованием функции-ключа"""
        self._items.sort(key=key_func, reverse=reverse)
        strategy_name = getattr(key_func, '__name__', str(key_func))
        print(f"✓ Отсортировано по: {strategy_name} (reverse={reverse})")
        return self
    
    def sort_by_name(self, reverse: bool = False) -> 'PatientRegistry':
        return self.sort_by(st.by_full_name, reverse)
    
    def sort_by_age(self, reverse: bool = False) -> 'PatientRegistry':
        return self.sort_by(st.by_age, reverse)
    
    def sort_by_temperature(self, reverse: bool = False) -> 'PatientRegistry':
        return self.sort_by(st.by_temperature, reverse)
    
    # ---------- Фильтрация (возвращает новую коллекцию) ----------
    def filter_by(self, predicate: Callable) -> 'PatientRegistry':
        new_registry = PatientRegistry()
        new_registry._items = list(filter(predicate, self._items))
        filter_name = getattr(predicate, '__name__', str(predicate))
        print(f"✓ Отфильтровано по: {filter_name} (осталось {len(new_registry)})")
        return new_registry
    
    def get_active(self) -> 'PatientRegistry':
        return self.filter_by(st.is_active)
    
    def get_emergency(self) -> 'PatientRegistry':
        return self.filter_by(st.is_emergency)
    
    def get_critical(self) -> 'PatientRegistry':
        return self.filter_by(st.is_critical)
    
    def filter_by_temperature_range(self, min_temp: float, max_temp: float) -> 'PatientRegistry':
        return self.filter_by(st.make_temperature_filter(min_temp, max_temp))
    
    def filter_by_age_range(self, min_age: int, max_age: int) -> 'PatientRegistry':
        return self.filter_by(st.make_age_filter(min_age, max_age))
    
    # ---------- Применение функции ко всем элементам ----------
    def apply(self, func: Callable) -> 'PatientRegistry':
        for i, patient in enumerate(self._items):
            result = func(patient)
            if isinstance(result, Patient) and result is not patient:
                self._items[i] = result
        func_name = getattr(func, '__name__', str(func))
        print(f"✓ Применена функция: {func_name}")
        return self
    
    def map_to(self, transform_func: Callable) -> List:
        result = list(map(transform_func, self._items))
        func_name = getattr(transform_func, '__name__', str(transform_func))
        print(f"✓ Преобразовано с помощью: {func_name}")
        return result
    
    # ---------- Цепочки ----------
    def chain(self) -> 'PatientRegistryChain':
        return PatientRegistryChain(self)
    
    # ---------- Вспомогательные ----------
    def clear(self) -> None:
        count = len(self._items)
        self._items.clear()
        print(f"✓ Коллекция очищена (удалено {count})")
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self) -> Iterator[Patient]:
        return iter(self._items)
    
    def __getitem__(self, index) -> Patient:
        return self._items[index]
    
    def __contains__(self, patient: Patient) -> bool:
        return patient in self._items
    
    def __str__(self) -> str:
        if not self._items:
            return "PatientRegistry (пусто)"
        result = f"\n📋 PatientRegistry ({len(self._items)} пациентов):\n" + "=" * 70 + "\n"
        for i, p in enumerate(self._items, 1):
            result += f"{i:2}. {str(p)[:65]}\n"
        result += "=" * 70
        return result


class PatientRegistryChain:
    """Для построения цепочек операций"""
    def __init__(self, registry: PatientRegistry):
        self._registry = registry
        self._current = registry
    
    def filter(self, predicate: Callable) -> 'PatientRegistryChain':
        self._current = self._current.filter_by(predicate)
        return self
    
    def sort(self, key_func: Callable, reverse: bool = False) -> 'PatientRegistryChain':
        self._current.sort_by(key_func, reverse)
        return self
    
    def apply(self, func: Callable) -> 'PatientRegistryChain':
        self._current.apply(func)
        return self
    
    def result(self) -> PatientRegistry:
        return self._current