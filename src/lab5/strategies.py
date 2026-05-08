"""
ЛР-5: Функции как аргументы. Стратегии и делегаты.
Файл содержит стратегии сортировки, фильтрации и обработки объектов Patient
"""


from typing import List, Callable
from base import Patient
from models import EmergencyPatient
from models import ChronicPatient


# ============ СТРАТЕГИИ СОРТИРОВКИ ============

def by_full_name(patient: Patient) -> str:
    """
    Стратегия сортировки по ФИО (алфавитный порядок)
    """
    return patient.full_name


def by_age(patient: Patient) -> int:
    """
    Стратегия сортировки по возрасту
    """
    return patient.age


def by_temperature(patient: Patient) -> float:
    """
    Стратегия сортировки по температуре тела
    """
    return patient.temperature


def by_days_in_hospital(patient: Patient) -> int:
    """
    Стратегия сортировки по количеству дней в больнице
    """
    return patient.days_in_hospital


def by_severity(patient: Patient) -> int:
    """
    Стратегия сортировки по степени тяжести (для экстренных пациентов)
    Для обычных пациентов возвращает 0
    """
    if hasattr(patient, 'severity'):
        return patient.severity
    return 0  # Обычные пациенты считаются с минимальной тяжестью


def by_chronic_years(patient: Patient) -> int:
    """
    Стратегия сортировки по стажу хронического заболевания
    """
    if hasattr(patient, 'years_with_disease'):
        return patient.years_with_disease
    return 0


def by_multiple_criteria(patient: Patient) -> tuple:
    """
    Стратегия сортировки по нескольким критериям:
    сначала по статусу (выписанные в конец), затем по температуре (от высокой к низкой)
    """
    # Статус: 0 - на лечении, 1 - направлен, 2 - выписан
    status_order = {"на лечении": 0, "направлен": 1, "выписан": 2}
    return (status_order.get(patient.status, 0), -patient.temperature)


# ============ ФУНКЦИИ-ФИЛЬТРЫ ============

def is_critical(patient: Patient) -> bool:
    """
    Фильтр: критические пациенты (температура >= 39.0 или экстренные с тяжестью >= 4)
    """
    if patient.has_fever() and patient.temperature >= 39.0:
        return True
    if hasattr(patient, 'severity') and patient.severity >= 4:
        return True
    return False


def is_normal_temp(patient: Patient) -> bool:
    """
    Фильтр: пациенты с нормальной температурой (<= 36.9)
    """
    return patient.is_temperature_normal()


def is_emergency(patient: Patient) -> bool:
    """
    Фильтр: только экстренные пациенты
    """
    return isinstance(patient, EmergencyPatient)


def is_chronic(patient: Patient) -> bool:
    """
    Фильтр: только хронические пациенты
    """
    return isinstance(patient, ChronicPatient)


def is_active(patient: Patient) -> bool:
    """
    Фильтр: пациенты на лечении (не выписанные)
    """
    return patient.status != "выписан"


# ============ ФУНКЦИИ-ОБРАБОТЧИКИ ДЛЯ MAP ============

def to_info_dict(patient: Patient) -> dict:
    """
    Преобразование пациента в словарь с ключевой информацией
    """
    return {
        "id": patient.patient_id,
        "name": patient.full_name,
        "age": patient.age,
        "diagnosis": patient.diagnosis,
        "temperature": patient.temperature,
        "status": patient.status
    }


def to_short_string(patient: Patient) -> str:
    """
    Краткое строковое представление пациента
    """
    return f"{patient.full_name} ({patient.age} лет) - {patient.diagnosis}"


def apply_discount_to_cost(patient: Patient, discount: float = 0.1) -> float:
    """
    Применение скидки к стоимости лечения
    """
    return patient.calculate_treatment_cost() * (1 - discount)


def mark_as_visited(patient: Patient) -> Patient:
    """
    Отметить пациента как осмотренного (изменяет диагноз)
    """
    if patient.diagnosis.startswith("ОСМОТРЕН: "):
        return patient
    patient.diagnosis = f"ОСМОТРЕН: {patient.diagnosis}"
    return patient


# ============ ФАБРИКИ ФУНКЦИЙ ============

def make_temperature_filter(min_temp: float, max_temp: float) -> Callable[[Patient], bool]:
    """
    Фабрика функций: создает фильтр по диапазону температур
    
    Args:
        min_temp: минимальная температура (включительно)
        max_temp: максимальная температура (включительно)
    
    Returns:
        Функция-фильтр, проверяющая попадает ли температура пациента в диапазон
    """
    def temperature_filter(patient: Patient) -> bool:
        return min_temp <= patient.temperature <= max_temp
    
    return temperature_filter


def make_age_filter(min_age: int, max_age: int) -> Callable[[Patient], bool]:
    """
    Фабрика функций: создает фильтр по возрастному диапазону
    
    Args:
        min_age: минимальный возраст (включительно)
        max_age: максимальный возраст (включительно)
    
    Returns:
        Функция-фильтр для проверки возраста
    """
    def age_filter(patient: Patient) -> bool:
        return min_age <= patient.age <= max_age
    
    return age_filter


def make_emergency_multiplier(severity_weight: float = 0.3) -> Callable[[Patient], float]:
    """
    Фабрика функций: создаёт функцию для расчёта веса пациента для сортировки
    Экстренные пациенты получают дополнительный вес
    
    Returns:
        Функция, возвращающая вес пациента (чем больше, тем важнее)
    """
    def calculate_weight(patient: Patient) -> float:
        base_weight = patient.age / 100  # нормализованный возраст
        if isinstance(patient, EmergencyPatient):
            base_weight += patient.severity * severity_weight
        return base_weight
    
    return calculate_weight


# ============ ПАТТЕРН СТРАТЕГИЯ (callable-объекты) ============

class SortingStrategy:
    """
    Абстрактная стратегия сортировки
    """
    def __call__(self, patient: Patient):
        raise NotImplementedError("Дочерний класс должен реализовать метод __call__")


class SortByNameStrategy(SortingStrategy):
    """Стратегия сортировки по имени"""
    
    def __call__(self, patient: Patient):
        return patient.full_name
    
    def __str__(self):
        return "Сортировка по ФИО"


class SortByAgeStrategy(SortingStrategy):
    """Стратегия сортировки по возрасту"""
    
    def __call__(self, patient: Patient):
        return patient.age
    
    def __str__(self):
        return "Сортировка по возрасту"


class SortByPriorityStrategy(SortingStrategy):
    """
    Стратегия сортировки по приоритету:
    1. Критические пациенты (высокая температура или тяжесть)
    2. Экстренные пациенты
    3. Остальные
    """
    
    def __call__(self, patient: Patient) -> tuple:
        priority = 3
        if is_critical(patient):
            priority = 1
        elif isinstance(patient, EmergencyPatient):
            priority = 2
        return (priority, patient.admission_date)
    
    def __str__(self):
        return "Сортировка по приоритету (критические → экстренные → остальные)"


class TreatmentStrategy:
    """Стратегия обработки пациента (apply)"""
    
    def __init__(self, action_name: str):
        self.action_name = action_name
    
    def __call__(self, patient: Patient) -> Patient:
        print(f"  → {self.action_name} для {patient.full_name}")
        return patient