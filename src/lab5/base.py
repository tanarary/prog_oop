"""
Базовый класс Patient из лабораторной работы №1
"""
import re
from datetime import datetime


def validate_full_name(name):
    """Проверка ФИО"""
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
    """Проверка возраста"""
    if not isinstance(age, int):
        raise TypeError("Возраст должен быть целым числом")
    if age < 0 or age > 120:
        raise ValueError("Возраст должен быть от 0 до 120 лет")
    return age


def validate_blood_type(blood_type):
    """Проверка группы крови"""
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
    """Проверка диагноза"""
    if not isinstance(diagnosis, str):
        raise TypeError("Диагноз должен быть строкой")
    
    diagnosis = diagnosis.strip()
    if not diagnosis:
        raise ValueError("Диагноз не может быть пустым")
    if len(diagnosis) < 3:
        raise ValueError("Диагноз должен содержать минимум 3 символа")
    
    return diagnosis


def validate_temperature(temp):
    """Проверка температуры"""
    if not isinstance(temp, (int, float)):
        raise TypeError("Температура должна быть числом")
    if temp < 35.0 or temp > 42.0:
        raise ValueError("Температура должна быть от 35.0 до 42.0°C")
    return round(float(temp), 1)


def validate_status(status):
    """Проверка статуса"""
    valid_statuses = ["на лечении", "выписан", "направлен"]
    if status not in valid_statuses:
        raise ValueError(f"Статус должен быть одним из: {', '.join(valid_statuses)}")
    return status


class Patient:
    """Базовый класс пациента"""
    
    total_patients = 0
    hospital_name = "Городская больница №1"
    
    MIN_TEMP_FOR_FEVER = 37.2
    MAX_NORMAL_TEMP = 36.9
    
    def __init__(self, full_name, age, blood_type, diagnosis, temperature=36.6):
        """Конструктор пациента"""
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
    
    # ---------- Геттеры ----------
    @property
    def full_name(self):
        return self._full_name
    
    @property
    def age(self):
        return self._age
    
    @property
    def blood_type(self):
        return self._blood_type
    
    @property
    def diagnosis(self):
        return self._diagnosis
    
    @property
    def temperature(self):
        return self._temperature
    
    @property
    def status(self):
        return self._status
    
    @property
    def patient_id(self):
        return self._patient_id
    
    @property
    def admission_date(self):
        return self._admission_date
    
    @property
    def discharge_date(self):
        return self._discharge_date
    
    @property
    def days_in_hospital(self):
        """Количество дней в больнице"""
        if self._status == "выписан" and self._discharge_date:
            return (self._discharge_date - self._admission_date).days
        return (datetime.now() - self._admission_date).days
    
    # ---------- Сеттеры ----------
    @diagnosis.setter
    def diagnosis(self, value):
        """Изменение диагноза"""
        if self._status == "выписан":
            raise ValueError("Нельзя изменить диагноз выписанному пациенту")
        
        old_diagnosis = self._diagnosis
        self._diagnosis = validate_diagnosis(value)
        print(f"Диагноз изменен: '{old_diagnosis}' -> '{self._diagnosis}'")
    
    @temperature.setter
    def temperature(self, value):
        """Изменение температуры"""
        self._temperature = validate_temperature(value)
        
        if self.has_fever():
            print(f"⚠️ У пациента повышенная температура ({self._temperature}°C)")
        else:
            print(f"Температура измерена: {self._temperature}°C")
    
    # ---------- Методы изменения состояния ----------
    def discharge(self):
        """Выписать пациента"""
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
        """Направить к специалисту"""
        if self._status == "выписан":
            raise ValueError("Нельзя направить выписанного пациента")
        
        self._status = "направлен"
        print(f"📋 Пациент {self._full_name} направлен к {specialist}")
    
    # ---------- Медицинские проверки ----------
    def has_fever(self):
        """Проверка лихорадки"""
        return self._temperature >= Patient.MIN_TEMP_FOR_FEVER
    
    def is_temperature_normal(self):
        """Проверка нормальной температуры"""
        return self._temperature <= Patient.MAX_NORMAL_TEMP
    
    def can_donate_blood(self):
        """Проверка возможности донорства"""
        reasons = []
        
        if self._age < 18:
            reasons.append("возраст меньше 18 лет")
        if self._age > 60:
            reasons.append("возраст больше 60 лет")
        if self._status != "выписан":
            reasons.append(f"статус: {self._status}")
        if self.has_fever():
            reasons.append(f"повышенная температура ({self._temperature}°C)")
        if self._blood_type == "не указана":
            reasons.append("не указана группа крови")
        
        if reasons:
            return False, f"Не может сдавать кровь: {', '.join(reasons)}"
        return True, "Может сдавать кровь"
    
    def get_health_status(self):
        """Получить статус здоровья"""
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
    
    # ---------- Метод для полиморфизма ----------
    def calculate_treatment_cost(self):
        """
        Расчет стоимости лечения.
        Будет переопределен в дочерних классах.
        """
        base_cost = 1000 * self.days_in_hospital
        return base_cost
    
    # ---------- Специальные методы ----------
    def __str__(self):
        """Для пациентов и медперсонала"""
        admission_str = self._admission_date.strftime("%d.%m.%Y %H:%M")
        
        return (f"{self._full_name} (ID: {self._patient_id}) | "
                f"{self._age} лет | Гр.крови: {self._blood_type} | "
                f"{self._temperature}°C | "
                f"📌 {self._diagnosis} | "
                f"📅 Поступление: {admission_str} | "
                f"{self.get_health_status()}")
    
    def __repr__(self):
        """Для разработчиков"""
        return (f"Patient(full_name='{self._full_name}', age={self._age}, "
                f"blood_type='{self._blood_type}', diagnosis='{self._diagnosis}', "
                f"temperature={self._temperature}, status='{self._status}')")
    
    def __eq__(self, other):
        """Сравнение по ID"""
        if not isinstance(other, Patient):
            return NotImplemented
        return self._patient_id == other._patient_id
    
    def __lt__(self, other):
        """Сортировка по дате поступления"""
        if not isinstance(other, Patient):
            return NotImplemented
        return self._admission_date < other._admission_date