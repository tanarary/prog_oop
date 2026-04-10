"""
Производные классы от Patient
"""
from base import Patient


class EmergencyPatient(Patient):
    """
    Пациент скорой помощи (экстренный)
    Новые атрибуты: severity, ambulance_arrival_time
    Новый метод: requires_resuscitation()
    """
    
    def __init__(self, full_name, age, blood_type, diagnosis, 
                 severity, temperature=36.6):
        # super() - вызов конструктора базового класса
        super().__init__(full_name, age, blood_type, diagnosis, temperature)
        
        # Новые атрибуты
        self._severity = self._validate_severity(severity)
        
        print(f"🚑 ЭКСТРЕННЫЙ пациент, степень тяжести: {self._severity}")
    
    @staticmethod
    def _validate_severity(value):
        if not isinstance(value, int):
            raise TypeError("Степень тяжести должна быть целым числом")
        if value < 1 or value > 5:
            raise ValueError("Степень тяжести должна быть от 1 до 5")
        return value
    
    # Новый метод дочернего класса
    def requires_resuscitation(self):
        """Требуется ли реанимация"""
        return self._severity >= 4
    
    # Переопределение метода calculate_treatment_cost (полиморфизм)
    def calculate_treatment_cost(self):
        base_cost = super().calculate_treatment_cost()
        severity_multiplier = 1 + (self._severity * 0.2)
        emergency_fee = 5000
        return round((base_cost * severity_multiplier) + emergency_fee, 2)
    
    # Переопределение __str__
    def __str__(self):
        base_str = super().__str__()
        return f"🚑 ЭКСТРЕННЫЙ (тяжесть {self._severity}/5) | {base_str}"
    
    @property
    def severity(self):
        return self._severity


class ChronicPatient(Patient):
    """
    Пациент с хроническим заболеванием
    Новые атрибуты: chronic_disease, years_with_disease
    Новый метод: is_in_exacerbation()
    """
    
    def __init__(self, full_name, age, blood_type, diagnosis, 
                 chronic_disease, years_with_disease, temperature=36.6):
        # super() - вызов конструктора базового класса
        super().__init__(full_name, age, blood_type, diagnosis, temperature)
        
        # Новые атрибуты
        self._chronic_disease = self._validate_chronic_disease(chronic_disease)
        self._years_with_disease = self._validate_years_with_disease(years_with_disease, age)
        
        print(f"📋 ХРОНИЧЕСКИЙ пациент: {self._chronic_disease} ({self._years_with_disease} лет)")
    
    @staticmethod
    def _validate_chronic_disease(value):
        if not isinstance(value, str):
            raise TypeError("Хроническое заболевание должно быть строкой")
        value = value.strip()
        if not value:
            raise ValueError("Хроническое заболевание не может быть пустым")
        return value
    
    def _validate_years_with_disease(self, years, age):
        if not isinstance(years, (int, float)):
            raise TypeError("Количество лет должно быть числом")
        if years < 0 or years > age:
            raise ValueError("Некорректное количество лет с заболеванием")
        return years
    
    # Новый метод дочернего класса
    def is_in_exacerbation(self):
        """Проверка обострения по температуре"""
        return self.has_fever() and self._temperature >= 38.0
    
    # Переопределение метода calculate_treatment_cost (полиморфизм)
    def calculate_treatment_cost(self):
        base_cost = super().calculate_treatment_cost()
        therapy_cost = 2000 * (self._years_with_disease // 5 + 1)
        
        if self.is_in_exacerbation():
            therapy_cost *= 1.5
        
        return round(base_cost + therapy_cost, 2)
    
    # Переопределение __str__
    def __str__(self):
        base_str = super().__str__()
        marker = "⚠️ ОБОСТРЕНИЕ ⚠️" if self.is_in_exacerbation() else "📋 ХРОНИЧЕСКИЙ"
        return f"{marker} | {base_str} | Болеет: {self._years_with_disease} лет"
    
    @property
    def chronic_disease(self):
        return self._chronic_disease
    
    @property
    def years_with_disease(self):
        return self._years_with_disease