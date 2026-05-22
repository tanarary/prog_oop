"""Бизнес-логика приложения: управление коллекцией пациентов."""

import sys
import os

# Добавляем пути для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from typing import List, Optional, Callable
from lab3.base import Patient
from lab3.models import EmergencyPatient
from lab3.models import ChronicPatient
from lab5.collection import PatientRegistry
from lab5.strategies import (
    by_full_name, by_age, by_temperature,
    is_active, is_emergency, is_critical,
    make_temperature_filter, make_age_filter
)
from .exceptions import PatientNotFoundError, DuplicatePatientError, InvalidPatientDataError


class PatientApp:
    """Основной класс приложения, связывающий коллекцию и бизнес-операции."""

    def __init__(self, registry: PatientRegistry):
        self._registry = registry

    # ---------- Основные операции ----------
    def add_patient(self, full_name: str, age: int, blood_type: str,
                    diagnosis: str, temperature: float,
                    patient_type: str = "base", **kwargs) -> Patient:
        """
        Добавить пациента.
        patient_type: "base", "emergency", "chronic"
        Для emergency: severity (int)
        Для chronic: chronic_disease (str), years_with_disease (int)
        """
        try:
            if patient_type == "emergency":
                severity = kwargs.get("severity")
                if severity is None:
                    raise InvalidPatientDataError("Для экстренного пациента укажите severity")
                patient = EmergencyPatient(full_name, age, blood_type, diagnosis, severity, temperature)
            elif patient_type == "chronic":
                chronic_disease = kwargs.get("chronic_disease")
                years = kwargs.get("years_with_disease")
                if not chronic_disease or years is None:
                    raise InvalidPatientDataError("Для хронического пациента укажите chronic_disease и years_with_disease")
                patient = ChronicPatient(full_name, age, blood_type, diagnosis, chronic_disease, years, temperature)
            else:
                patient = Patient(full_name, age, blood_type, diagnosis, temperature)
            self._registry.add(patient)
            return patient
        except ValueError as e:
            raise InvalidPatientDataError(str(e))
        except Exception as e:
            if "уже существует" in str(e):
                raise DuplicatePatientError(str(e))
            raise

    def remove_patient(self, patient_id: int, confirm: bool = False) -> Patient:
        """Удалить пациента по ID. Если confirm=False, выбросить исключение (для подтверждения)."""
        patient = self.find_by_id(patient_id)
        if patient is None:
            raise PatientNotFoundError(f"Пациент с ID {patient_id} не найден")
        if not confirm:
            raise ValueError("need_confirm")  # специальный сигнал для CLI
        self._registry.remove(patient)
        return patient

    def update_diagnosis(self, patient_id: int, new_diagnosis: str) -> Patient:
        """Изменить диагноз пациента."""
        patient = self.find_by_id(patient_id)
        if patient is None:
            raise PatientNotFoundError(f"Пациент с ID {patient_id} не найден")
        patient.diagnosis = new_diagnosis
        return patient

    def find_by_id(self, patient_id: int) -> Optional[Patient]:
        """Поиск по ID."""
        return self._registry.find_by_id(patient_id)

    def find_by_name(self, substring: str) -> List[Patient]:
        """Поиск по части ФИО."""
        return self._registry.find_by_name(substring)

    def get_all_patients(self) -> List[Patient]:
        """Получить всех пациентов."""
        return self._registry.get_all()

    # ---------- Фильтрация (возвращает новый реестр) ----------
    def filter_active(self) -> PatientRegistry:
        return self._registry.filter_by(is_active)

    def filter_emergency(self) -> PatientRegistry:
        return self._registry.filter_by(is_emergency)

    def filter_critical(self) -> PatientRegistry:
        return self._registry.filter_by(is_critical)

    def filter_by_temperature(self, min_temp: float, max_temp: float) -> PatientRegistry:
        predicate = make_temperature_filter(min_temp, max_temp)
        return self._registry.filter_by(predicate)

    def filter_by_age(self, min_age: int, max_age: int) -> PatientRegistry:
        predicate = make_age_filter(min_age, max_age)
        return self._registry.filter_by(predicate)

    # ---------- Сортировка (in-place, возвращает ссылку на себя) ----------
    def sort_by_name(self, reverse: bool = False) -> PatientRegistry:
        return self._registry.sort_by(by_full_name, reverse)

    def sort_by_age(self, reverse: bool = False) -> PatientRegistry:
        return self._registry.sort_by(by_age, reverse)

    def sort_by_temperature(self, reverse: bool = False) -> PatientRegistry:
        return self._registry.sort_by(by_temperature, reverse)

    # ---------- Дополнительно ----------
    def get_registry(self) -> PatientRegistry:
        return self._registry

    def count(self) -> int:
        return len(self._registry)