"""
Лабораторная работа №4 - Модели данных с поддержкой интерфейсов
На основе ЛР2, но с реализацией Printable и Comparable
"""

import re
from datetime import datetime
from typing import Optional, Union, Callable, List
from interfaces import Printable, Comparable


# ============ ВАЛИДАЦИИ (без изменений) ============
def validate_full_name(name):
    if not isinstance(name, str):
        raise TypeError("ФИО должно быть строкой")
    name = name.strip()
    if not name:
        raise ValueError("ФИО не может быть пустым")
    parts = name.split()
    if len(parts) < 2:
        raise ValueError("ФИО должно содержать минимум имя и фамилию")
    for part in parts:
        if not re.match(r"^[А-Яа-яA-Za-z-]+$", part):
            raise ValueError(f"Часть ФИО '{part}' содержит недопустимые символы")
        if len(part) < 2:
            raise ValueError(f"Часть ФИО '{part}' слишком короткая")
    return name


def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Возраст должен быть целым числом")
    if age < 0 or age > 120:
        raise ValueError("Возраст должен быть от 0 до 120 лет")
    return age


def validate_blood_type(blood_type):
    valid_types = ["1", "2", "3", "4", "A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-", "не указана"]
    if not isinstance(blood_type, str):
        raise TypeError("Группа крови должна быть строкой")
    if blood_type not in valid_types:
        raise ValueError(f"Группа крови должна быть одной из: {', '.join(valid_types)}")
    return blood_type


def validate_diagnosis(diagnosis):
    if not isinstance(diagnosis, str):
        raise TypeError("Диагноз должен быть строкой")
    diagnosis = diagnosis.strip()
    if not diagnosis:
        raise ValueError("Диагноз не может быть пустым")
    if len(diagnosis) < 3:
        raise ValueError("Диагноз должен содержать минимум 3 символа")
    return diagnosis


def validate_temperature(temp):
    if not isinstance(temp, (int, float)):
        raise TypeError("Температура должна быть числом")
    if temp < 35.0 or temp > 42.0:
        raise ValueError("Температура должна быть от 35.0 до 42.0°C")
    return round(float(temp), 1)


def validate_status(status):
    valid_statuses = ["на лечении", "выписан", "направлен"]
    if status not in valid_statuses:
        raise ValueError(f"Статус должен быть одним из: {', '.join(valid_statuses)}")
    return status


# ============ КЛАСС PATIENT (с интерфейсами) ============
class Patient(Printable, Comparable):
    """Класс пациента с поддержкой интерфейсов Printable и Comparable"""
    
    total_patients = 0
    hospital_name = "Городская больница №1"
    
    MIN_TEMP_FOR_FEVER = 37.2
    MAX_NORMAL_TEMP = 36.9
    
    def __init__(self, full_name, age, blood_type, diagnosis, temperature=36.6):
        self._full_name = validate_full_name(full_name)
        self._age = validate_age(age)
        self._blood_type = validate_blood_type(blood_type)
        self._diagnosis = validate_diagnosis(diagnosis)
        self._temperature = validate_temperature(temperature)
        self._status = "на лечении"
        self._admission_date = datetime.now()
        self._discharge_date = None
        
        Patient.total_patients += 1
        self._patient_id = Patient.total_patients
        
        print(f"Пациент {self._full_name} поступил в клинику (ID: {self._patient_id})")
    
    # ============ Геттеры ============
    @property
    def full_name(self): return self._full_name
    @property
    def age(self): return self._age
    @property
    def blood_type(self): return self._blood_type
    @property
    def diagnosis(self): return self._diagnosis
    @property
    def temperature(self): return self._temperature
    @property
    def status(self): return self._status
    @property
    def patient_id(self): return self._patient_id
    @property
    def admission_date(self): return self._admission_date
    @property
    def discharge_date(self): return self._discharge_date
    
    @property
    def days_in_hospital(self):
        if self._status == "выписан" and self._discharge_date:
            return (self._discharge_date - self._admission_date).days
        return (datetime.now() - self._admission_date).days
    
    # ============ Сеттеры ============
    @diagnosis.setter
    def diagnosis(self, value):
        if self._status == "выписан":
            raise ValueError("Нельзя изменить диагноз выписанному пациенту")
        old_diagnosis = self._diagnosis
        self._diagnosis = validate_diagnosis(value)
        print(f"Диагноз изменен: '{old_diagnosis}' -> '{self._diagnosis}'")
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = validate_temperature(value)
        if self.has_fever():
            print(f"⚠️ У пациента повышенная температура ({self._temperature}°C)")
    
    # ============ Методы изменения состояния ============
    def discharge(self):
        if self._status == "выписан":
            print("Пациент уже выписан")
            return
        if self._status != "на лечении":
            raise ValueError("Можно выписать только пациента на лечении")
        if self.has_fever():
            raise ValueError("Нельзя выписать пациента с температурой")
        self._status = "выписан"
        self._discharge_date = datetime.now()
        print(f"✅ Пациент {self._full_name} выписан. Дней в стационаре: {self.days_in_hospital}")
    
    def refer_to_specialist(self, specialist):
        if self._status == "выписан":
            raise ValueError("Нельзя направить выписанного пациента")
        self._status = "направлен"
        print(f"📋 Пациент {self._full_name} направлен к {specialist}")
    
    # ============ Медицинские проверки ============
    def has_fever(self):
        return self._temperature >= Patient.MIN_TEMP_FOR_FEVER
    
    def is_temperature_normal(self):
        return self._temperature <= Patient.MAX_NORMAL_TEMP
    
    def can_donate_blood(self):
        reasons = []
        if self._age < 18: reasons.append("возраст меньше 18 лет")
        if self._age > 60: reasons.append("возраст больше 60 лет")
        if self._status != "выписан": reasons.append(f"статус: {self._status}")
        if self.has_fever(): reasons.append(f"повышенная температура ({self._temperature}°C)")
        if self._blood_type == "не указана": reasons.append("не указана группа крови")
        if reasons:
            return False, f"Не может сдавать кровь: {', '.join(reasons)}"
        return True, "Может сдавать кровь"
    
    def get_health_status(self):
        statuses = []
        if self.has_fever():
            statuses.append("🌡️ Лихорадка")
        elif self.is_temperature_normal():
            statuses.append("✅ Температура в норме")
        else:
            statuses.append("⚠️ Температура слегка повышена")
        if self._status == "на лечении":
            statuses.append("💊 На лечении")
        elif self._status == "выписан":
            statuses.append("🏠 Выписан")
        elif self._status == "направлен":
            statuses.append("👨‍⚕️ Направлен к специалисту")
        return " | ".join(statuses)
    
    # ============ РЕАЛИЗАЦИЯ ИНТЕРФЕЙСА Printable ============
    def to_string(self, format_type: str = "default") -> str:
        """Разные форматы вывода в зависимости от format_type"""
        if format_type == "short":
            return f"{self._patient_id}: {self._full_name}"
        elif format_type == "detailed":
            return (f"=== КАРТА ПАЦИЕНТА №{self._patient_id} ===\n"
                    f"ФИО: {self._full_name}\n"
                    f"Возраст: {self._age} лет\n"
                    f"Группа крови: {self._blood_type}\n"
                    f"Диагноз: {self._diagnosis}\n"
                    f"Температура: {self._temperature}°C\n"
                    f"Статус: {self._status}\n"
                    f"Дата поступления: {self._admission_date.strftime('%d.%m.%Y %H:%M')}\n"
                    f"Дней в стационаре: {self.days_in_hospital}")
        else:  # default
            admission_str = self._admission_date.strftime("%d.%m.%Y %H:%M")
            return (f"{self._full_name} (ID: {self._patient_id}) | "
                    f"{self._age} лет | {self._temperature}°C | "
                    f"{self._diagnosis} | {self.get_health_status()}")
    
    def to_short_string(self) -> str:
        """Краткое представление для списков"""
        temp_marker = "🔥" if self.has_fever() else "✅"
        return f"[{self._patient_id}] {self._full_name} ({self._age}г) {temp_marker}"
    
    # ============ РЕАЛИЗАЦИЯ ИНТЕРФЕЙСА Comparable ============
    def compare_to(self, other) -> int:
        """Сравнение пациентов по ID"""
        if not isinstance(other, Patient):
            raise TypeError(f"Нельзя сравнить Patient с {type(other).__name__}")
        if self._patient_id < other._patient_id:
            return -1
        elif self._patient_id > other._patient_id:
            return 1
        return 0
    
    def get_sort_key(self) -> str:
        """Ключ для сортировки по ФИО + возрасту"""
        return f"{self._full_name}_{self._age}"
    
    # ============ Специальные методы ============
    def __str__(self):
        return self.to_string("default")
    
    def __repr__(self):
        return (f"Patient(full_name='{self._full_name}', age={self._age}, "
                f"blood_type='{self._blood_type}', diagnosis='{self._diagnosis}', "
                f"temperature={self._temperature}, status='{self._status}')")
    
    def __eq__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return self._patient_id == other._patient_id
    
    def __lt__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return self._admission_date < other._admission_date


# ============ КЛАСС PATIENT REGISTRY (обновленный) ============
class PatientRegistry:
    """Коллекция для хранения пациентов с поддержкой интерфейсов"""
    
    def __init__(self):
        self._items: List[Patient] = []
    
    def add(self, patient: Patient) -> None:
        if not isinstance(patient, Patient):
            raise TypeError(f"Можно добавлять только объекты Patient, получен {type(patient).__name__}")
        if self._find_by_id(patient.patient_id) is not None:
            raise ValueError(f"Пациент с ID {patient.patient_id} уже существует в коллекции")
        self._items.append(patient)
        print(f"✓ Пациент '{patient.full_name}' (ID: {patient.patient_id}) добавлен в реестр")
    
    def remove(self, patient: Patient) -> None:
        if patient not in self._items:
            raise ValueError(f"Пациент '{patient.full_name}' не найден в коллекции")
        self._items.remove(patient)
        print(f"✓ Пациент '{patient.full_name}' удален из реестра")
    
    def get_all(self) -> List[Patient]:
        return self._items.copy()
    
    def _find_by_id(self, patient_id: int):
        for patient in self._items:
            if patient.patient_id == patient_id:
                return patient
        return None
    
    def find_by_id(self, patient_id: int):
        result = self._find_by_id(patient_id)
        if result:
            print(f"🔍 Найден пациент: {result.full_name}")
        else:
            print(f"❌ Пациент с ID {patient_id} не найден")
        return result
    
    def find_by_name(self, name_substring: str) -> List[Patient]:
        name_substring = name_substring.lower()
        results = [p for p in self._items if name_substring in p.full_name.lower()]
        print(f"🔍 Найдено {len(results)} пациентов по запросу '{name_substring}':")
        for p in results:
            print(f"   - {p.full_name} (ID: {p.patient_id})")
        return results
    
    # ============ НОВЫЕ МЕТОДЫ ДЛЯ РАБОТЫ ЧЕРЕЗ ИНТЕРФЕЙСЫ ============
    def get_printable_items(self) -> List[Printable]:
        """Вернуть все объекты, реализующие Printable"""
        return [p for p in self._items if isinstance(p, Printable)]
    
    def get_comparable_items(self) -> List[Comparable]:
        """Вернуть все объекты, реализующие Comparable"""
        return [p for p in self._items if isinstance(p, Comparable)]
    
    def print_all_via_interface(self, format_type: str = "default") -> None:
        """Вывести всех пациентов через интерфейс Printable"""
        print(f"\n📋 ВЫВОД ЧЕРЕЗ ИНТЕРФЕЙС Printable (формат: {format_type}):")
        print("=" * 60)
        for item in self.get_printable_items():
            print(item.to_string(format_type))
        print("=" * 60)
    
    def sort_by_comparable(self, reverse: bool = False) -> 'PatientRegistry':
        """Сортировка через интерфейс Comparable"""
        self._items.sort(key=lambda p: p.get_sort_key(), reverse=reverse)
        print(f"✓ Коллекция отсортирована через Comparable (reverse={reverse})")
        return self
    
    # ============ Существующие методы (без изменений) ============
    def find_by_diagnosis(self, diagnosis_substring: str) -> List[Patient]:
        diagnosis_substring = diagnosis_substring.lower()
        results = [p for p in self._items if diagnosis_substring in p.diagnosis.lower()]
        print(f"🔍 Найдено {len(results)} пациентов с диагнозом, содержащим '{diagnosis_substring}':")
        for p in results:
            print(f"   - {p.full_name}: {p.diagnosis}")
        return results
    
    def find_by_status(self, status: str) -> List[Patient]:
        validate_status(status)
        results = [p for p in self._items if p.status == status]
        print(f"🔍 Найдено {len(results)} пациентов со статусом '{status}':")
        for p in results:
            print(f"   - {p.full_name}")
        return results
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __contains__(self, patient):
        return patient in self._items
    
    def __str__(self) -> str:
        if not self._items:
            return "PatientRegistry (пусто)"
        result = f"\n📋 PatientRegistry ({len(self._items)} пациентов):\n" + "="*60 + "\n"
        for i, patient in enumerate(self._items, 1):
            result += f"{i:2}. {patient.full_name:30} | {patient.diagnosis:20} | {patient.status}\n"
        result += "="*60
        return result
    
    def remove_at(self, index: int) -> Patient:
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        removed = self._items.pop(index)
        print(f"✓ Удален пациент по индексу {index}: '{removed.full_name}'")
        return removed
    
    def sort(self, key=None, reverse=False):
        if key is None:
            self._items.sort(reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)
        print(f"✓ Коллекция отсортирована (reverse={reverse})")
        return self
    
    def sort_by_name(self, reverse=False):
        self.sort(key=lambda p: p.full_name, reverse=reverse)
        return self
    
    def sort_by_age(self, reverse=False):
        self.sort(key=lambda p: p.age, reverse=reverse)
        return self
    
    def sort_by_temperature(self, reverse=False):
        self.sort(key=lambda p: p.temperature, reverse=reverse)
        return self
    
    def sort_by_admission_date(self, reverse=False):
        self.sort(key=lambda p: p.admission_date, reverse=reverse)
        return self
    
    def get_active(self) -> 'PatientRegistry':
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.status == "на лечении":
                new_registry._items.append(patient)
        print(f"✓ Создана новая коллекция: {len(new_registry)} пациентов на лечении")
        return new_registry
    
    def get_discharged(self) -> 'PatientRegistry':
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.status == "выписан":
                new_registry._items.append(patient)
        print(f"✓ Создана новая коллекция: {len(new_registry)} выписанных пациентов")
        return new_registry
    
    def get_with_fever(self) -> 'PatientRegistry':
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.has_fever():
                new_registry._items.append(patient)
        print(f"✓ Создана новая коллекция: {len(new_registry)} пациентов с лихорадкой")
        return new_registry
    
    def get_by_blood_type(self, blood_type: str) -> 'PatientRegistry':
        validate_blood_type(blood_type)
        new_registry = PatientRegistry()
        for patient in self._items:
            if patient.blood_type == blood_type:
                new_registry._items.append(patient)
        print(f"✓ Создана новая коллекция: {len(new_registry)} пациентов с группой {blood_type}")
        return new_registry
    
    def clear(self) -> None:
        count = len(self._items)
        self._items.clear()
        print(f"✓ Коллекция очищена (удалено {count} пациентов)")
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def print_all(self) -> 'PatientRegistry':
        print(self)
        return self