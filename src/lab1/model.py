
from validate import (
    validate_full_name, validate_age, validate_blood_type,
    validate_diagnosis, validate_temperature, validate_status
)
from datetime import datetime

class Patient:
  
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
    
    @property
    def full_name(self):
        """ФИО пациента (только чтение)"""
        return self._full_name
    
    @property
    def age(self):
        """Возраст (только чтение)"""
        return self._age
    
    @property
    def blood_type(self):
        """Группа крови (только чтение)"""
        return self._blood_type
    
    @property
    def diagnosis(self):
        """Текущий диагноз (чтение)"""
        return self._diagnosis
    
    @diagnosis.setter
    def diagnosis(self, value):
        """
        Сеттер для диагноза с проверкой
        Нельзя менять диагноз выписанному пациенту
        """
        if self._status == "выписан":
            raise ValueError("Нельзя изменить диагноз выписанному пациенту")
        
        old_diagnosis = self._diagnosis
        self._diagnosis = validate_diagnosis(value)
        print(f"Диагноз изменен: '{old_diagnosis}' -> '{self._diagnosis}'")
    
    @property
    def temperature(self):
        """Температура тела (чтение)"""
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        """
        Сеттер для температуры с проверкой
        """
        self._temperature = validate_temperature(value)
        

        if self.has_fever():
            print(f" У пациента повышенная температура ({self._temperature}°C)")
        else:
            print(f"Температура измерена: {self._temperature}°C")
    
    @property
    def status(self):
        """Статус пациента"""
        return self._status
    
    @property
    def patient_id(self):
        """ID пациента"""
        return self._patient_id
    
    @property
    def admission_date(self):
        """Дата поступления"""
        return self._admission_date
    
    @property
    def discharge_date(self):
        """Дата выписки"""
        return self._discharge_date
    
    @property
    def days_in_hospital(self):
        """Количество дней в больнице"""
        if self._status == "выписан" and self._discharge_date:
            return (self._discharge_date - self._admission_date).days
        return (datetime.now() - self._admission_date).days
    
    # ----- Методы изменения состояния -----
    def discharge(self):
        """
        Выписать пациента
        """
        if self._status == "выписан":
            print("Пациент уже выписан")
            return
        
        if self._status != "на лечении":
            raise ValueError("Можно выписать только пациента на лечении")
        
        if self.has_fever():
            raise ValueError("Нельзя выписать пациента с температурой")
        
        self._status = "выписан"
        self._discharge_date = datetime.now()
        print(f" Пациент {self._full_name} выписан. Дней в стационаре: {self.days_in_hospital}")
    
    def refer_to_specialist(self, specialist):
        """
        Направить к специалисту
        """
        if self._status == "выписан":
            raise ValueError("Нельзя направить выписанного пациента")
        
        self._status = "направлен"
        print(f" Пациент {self._full_name} направлен к {specialist}")
    

    def has_fever(self):
        """
        Проверка, есть ли у пациента лихорадка
        """
        return self._temperature >= Patient.MIN_TEMP_FOR_FEVER
    
    def is_temperature_normal(self):
        """
        Проверка нормальной температуры
        """
        return self._temperature <= Patient.MAX_NORMAL_TEMP
    
    def can_donate_blood(self):
        """
        Проверка, может ли пациент сдавать кровь
        """
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
        """
        Получить статус здоровья
        """
        statuses = []
        
        if self.has_fever():
            statuses.append("Лихорадка")
        elif self.is_temperature_normal():
            statuses.append("Температура в норме")
        else:
            statuses.append("Температура слегка повышена")
        
        if self._status == "на лечении":
            statuses.append(" На лечении")
        elif self._status == "выписан":
            statuses.append("Выписан")
        elif self._status == "направлен":
            statuses.append("Направлен к специалисту")
        
        return " | ".join(statuses)
    

    def __str__(self):
        """
        Для пациентов и медперсонала - понятное представление
        """
        admission_str = self._admission_date.strftime("%d.%m.%Y")
        
        return (f"{self._full_name} (ID: {self._patient_id}) | "
                f"{self._age} лет | Группа крови: {self._blood_type} | "
                f"{self._temperature}°C | "
                f" {self._diagnosis} | "
                f"Поступление: {admission_str} | "
                f"{self.get_health_status()}")
    
    def __repr__(self):
        """
        Для разработчиков
        """
        return (f"Patient(full_name='{self._full_name}', age={self._age}, "
                f"blood_type='{self._blood_type}', diagnosis='{self._diagnosis}', "
                f"temperature={self._temperature}, status='{self._status}')")
    
    def __eq__(self, other):
        """
        Сравнение пациентов по ID (уникальный идентификатор)
        """
        if not isinstance(other, Patient):
            return NotImplemented
        return self._patient_id == other._patient_id
    
    def __lt__(self, other):
        """
        Сравнение для сортировки по дате поступления
        """
        if not isinstance(other, Patient):
            return NotImplemented
        return self._admission_date < other._admission_date