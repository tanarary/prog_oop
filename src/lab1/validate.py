
import re
from datetime import datetime

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
    valid_types = [
        "1", "2", "3", "4",
        "A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-",
        "не указана"
    ]
    
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