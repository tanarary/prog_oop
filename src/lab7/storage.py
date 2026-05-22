"""Сохранение и загрузка коллекции пациентов в/из JSON."""
import sys
import os

# Добавляем пути для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from typing import List, Dict, Any
from lab3.base import Patient
from lab3.models import EmergencyPatient
from lab3.models import ChronicPatient
from lab5.collection import PatientRegistry


def _patient_to_dict(patient: Patient) -> Dict[str, Any]:
    """Преобразует объект Patient в словарь для JSON."""
    data = {
        "type": "base",
        "full_name": patient.full_name,
        "age": patient.age,
        "blood_type": patient.blood_type,
        "diagnosis": patient.diagnosis,
        "temperature": patient.temperature,
        "status": patient.status,
        "admission_date": patient.admission_date.isoformat(),
        "discharge_date": patient.discharge_date.isoformat() if patient.discharge_date else None,
    }
    if isinstance(patient, EmergencyPatient):
        data["type"] = "emergency"
        data["severity"] = patient.severity
    elif isinstance(patient, ChronicPatient):
        data["type"] = "chronic"
        data["chronic_disease"] = patient.chronic_disease
        data["years_with_disease"] = patient.years_with_disease
    return data


def _dict_to_patient(data: Dict[str, Any]) -> Patient:
    """Восстанавливает объект Patient из словаря."""
    from datetime import datetime

    patient_type = data.get("type", "base")
    full_name = data["full_name"]
    age = data["age"]
    blood_type = data["blood_type"]
    diagnosis = data["diagnosis"]
    temperature = data["temperature"]
    # Восстановление дат
    admission_date = datetime.fromisoformat(data["admission_date"])
    discharge_date = datetime.fromisoformat(data["discharge_date"]) if data["discharge_date"] else None

    if patient_type == "emergency":
        severity = data["severity"]
        patient = EmergencyPatient(full_name, age, blood_type, diagnosis, severity, temperature)
    elif patient_type == "chronic":
        chronic_disease = data["chronic_disease"]
        years = data["years_with_disease"]
        patient = ChronicPatient(full_name, age, blood_type, diagnosis, chronic_disease, years, temperature)
    else:
        patient = Patient(full_name, age, blood_type, diagnosis, temperature)

    # Восстановление служебных полей (id, даты, статус)
    patient._patient_id = data.get("id", patient.patient_id)  # если сохраняли id
    patient._status = data["status"]
    patient._admission_date = admission_date
    if discharge_date:
        patient._discharge_date = discharge_date
    return patient


def save_registry(registry: PatientRegistry, filepath: str) -> None:
    """Сохранить реестр пациентов в JSON-файл."""
    patients_list = [patient for patient in registry.get_all()]
    data = [_patient_to_dict(p) for p in patients_list]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_registry(filepath: str) -> PatientRegistry:
    """Загрузить реестр пациентов из JSON-файла. Если файл не существует, вернуть пустой реестр."""
    registry = PatientRegistry()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            patient = _dict_to_patient(item)
            registry.add(patient)
    except FileNotFoundError:
        pass
    return registry