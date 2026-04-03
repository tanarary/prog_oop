# collection.py
from model import Patient
from typing import List, Optional, Callable, Union


class PatientRegistry:
    """
    Коллекция для хранения пациентов
    Реализует требования 3, 4, 5
    """
    
    def __init__(self):
        """Инициализация пустой коллекции"""
        self._items: List[Patient] = []
    
    # ============ ЗАДАНИЕ 3 ============
    
    def add(self, patient: Patient) -> None:
        """
        Добавить пациента в коллекцию
        Проверяет тип и отсутствие дубликатов
        """
        if not isinstance(patient, Patient):
            raise TypeError(f"Можно добавлять только объекты Patient, получен {type(patient).__name__}")
        
        # Проверка на дубликат по ID
        if self._find_by_id(patient.patient_id) is not None:
            raise ValueError(f"Пациент с ID {patient.patient_id} уже существует в коллекции")
        
        self._items.append(patient)
        print(f"✓ Пациент '{patient.full_name}' (ID: {patient.patient_id}) добавлен в реестр")
    
    def remove(self, patient: Patient) -> None:
        """
        Удалить пациента из коллекции
        """
        if patient not in self._items:
            raise ValueError(f"Пациент '{patient.full_name}' не найден в коллекции")
        
        self._items.remove(patient)
        print(f"✓ Пациент '{patient.full_name}' удален из реестра")
    
    def get_all(self) -> List[Patient]:
        """
        Вернуть копию списка всех пациентов
        """
        return self._items.copy()
    
    # ============ ЗАДАНИЕ 4 ============
    
    def _find_by_id(self, patient_id: int) -> Optional[Patient]:
        """Внутренний поиск по ID"""
        for patient in self._items:
            if patient.patient_id == patient_id:
                return patient
        return None
    
    def find_by_id(self, patient_id: int) -> Optional[Patient]:
        """Поиск пациента по ID"""
        result = self._find_by_id(patient_id)
        if result:
            print(f"🔍 Найден пациент: {result.full_name}")
        else:
            print(f"❌ Пациент с ID {patient_id} не найден")
        return result
    
    def find_by_name(self, name_substring: str) -> List[Patient]:
        """Поиск по части ФИО"""
        name_substring = name_substring.lower()
        results = [p for p in self._items if name_substring in p.full_name.lower()]
        
        print(f"🔍 Найдено {len(results)} пациентов по запросу '{name_substring}':")
        for p in results:
            print(f"   - {p.full_name} (ID: {p.patient_id})")
        return results
    
    def find_by_diagnosis(self, diagnosis_substring: str) -> List[Patient]:
        """Поиск по части диагноза"""
        diagnosis_substring = diagnosis_substring.lower()
        results = [p for p in self._items if diagnosis_substring in p.diagnosis.lower()]
        
        print(f"🔍 Найдено {len(results)} пациентов с диагнозом, содержащим '{diagnosis_substring}':")
        for p in results:
            print(f"   - {p.full_name}: {p.diagnosis}")
        return results
    
    def find_by_status(self, status: str) -> List[Patient]:
        """Поиск по статусу"""
        from model import validate_status
        validate_status(status)
        results = [p for p in self._items if p.status == status]
        
        print(f"🔍 Найдено {len(results)} пациентов со статусом '{status}':")
        for p in results:
            print(f"   - {p.full_name}")
        return results
    
    # ============ ЗАДАНИЕ 5 ============
    
    def __len__(self) -> int:
        """Поддержка len()"""
        return len(self._items)
    
    def __iter__(self):
        """Поддержка итерации for item in collection"""
        return iter(self._items)
    
    def __getitem__(self, index: Union[int, slice]):
        """Поддержка индексации collection[index]"""
        return self._items[index]
    
    def __contains__(self, patient: Patient) -> bool:
        """Поддержка оператора in"""
        return patient in self._items
    
    def __str__(self) -> str:
        """Строковое представление"""
        if not self._items:
            return "PatientRegistry (пусто)"
        
        result = f"\n📋 PatientRegistry ({len(self._items)} пациентов):\n"
        result += "="*60 + "\n"
        for i, patient in enumerate(self._items, 1):
            result += f"{i:2}. {patient.full_name:30} | {patient.diagnosis:20} | {patient.status}\n"
        result += "="*60
        return result
    
    def remove_at(self, index: int) -> Patient:
        """Удаление по индексу"""
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        
        removed = self._items.pop(index)
        print(f"✓ Удален пациент по индексу {index}: '{removed.full_name}'")
        return removed
    
    def sort(self, key: Optional[Callable] = None, reverse: bool = False) -> 'PatientRegistry':
        """
        Универсальная сортировка
        ВОЗВРАЩАЕТ СЕБЯ ДЛЯ ЦЕПОЧЕК ВЫЗОВОВ
        """
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
        print(f"✓ Коллекция отсортирована (reverse={reverse})")
        return self  # Возвращаем self для цепочек вызовов
    
    def sort_by_name(self, reverse: bool = False) -> 'PatientRegistry':
        """Сортировка по ФИО"""
        self.sort(key=lambda p: p.full_name, reverse=reverse)
        return self  # Возвращаем self для цепочек вызовов
    
    def sort_by_age(self, reverse: bool = False) -> 'PatientRegistry':
        """Сортировка по возрасту"""
        self.sort(key=lambda p: p.age, reverse=reverse)
        return self  # Возвращаем self для цепочек вызовов
    
    def sort_by_temperature(self, reverse: bool = False) -> 'PatientRegistry':
        """Сортировка по температуре"""
        self.sort(key=lambda p: p.temperature, reverse=reverse)
        return self  # Возвращаем self для цепочек вызовов
    
    def sort_by_admission_date(self, reverse: bool = False) -> 'PatientRegistry':
        """Сортировка по дате поступления"""
        self.sort(key=lambda p: p.admission_date, reverse=reverse)
        return self  # Возвращаем self для цепочек вызовов
    
    # ---------- Логические операции (возвращают новые коллекции) ----------
    
    def get_active(self) -> 'PatientRegistry':
        """Получить пациентов на лечении"""
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.status == "на лечении":
                new_registry._items.append(patient)  # Добавляем без проверок
        print(f"✓ Создана новая коллекция: {len(new_registry)} пациентов на лечении")
        return new_registry
    
    def get_discharged(self) -> 'PatientRegistry':
        """Получить выписанных пациентов"""
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.status == "выписан":
                new_registry._items.append(patient)
        print(f"✓ Создана новая коллекция: {len(new_registry)} выписанных пациентов")
        return new_registry
    
    def get_with_fever(self) -> 'PatientRegistry':
        """Получить пациентов с лихорадкой"""
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.has_fever():
                new_registry._items.append(patient)
        print(f"✓ Создана новая коллекция: {len(new_registry)} пациентов с лихорадкой")
        return new_registry
    
    def get_by_blood_type(self, blood_type: str) -> 'PatientRegistry':
        """Получить пациентов с указанной группой крови"""
        from model import validate_blood_type
        validate_blood_type(blood_type)
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.blood_type == blood_type:
                new_registry._items.append(patient)
        print(f"✓ Создана новая коллекция: {len(new_registry)} пациентов с группой {blood_type}")
        return new_registry
    
    # ---------- Дополнительные методы ----------
    
    def clear(self) -> None:
        """Очистить коллекцию"""
        count = len(self._items)
        self._items.clear()
        print(f"✓ Коллекция очищена (удалено {count} пациентов)")
    
    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return len(self._items) == 0
    
    def print_all(self) -> 'PatientRegistry':
        """Красивый вывод всех пациентов"""
        print(self)
        return self  # Возвращаем self для цепочек вызовов