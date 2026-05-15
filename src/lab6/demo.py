"""
Лабораторная работа №6 - Демонстрация работы с Generics и Protocol
Тема: Медицинская информационная система
"""
import sys
import os

# Добавляем пути для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем из правильных путей
from lab3.base import Patient
from lab6.container import TypedCollection, D, S, Displayable, Scorable


# ============ МЕДИЦИНСКИЕ КЛАССЫ ДЛЯ ДЕМОНСТРАЦИИ ПРОТОКОЛОВ ============

class MedicalRecord:
    """Медицинская карта пациента (для демонстрации Displayable)"""
    def __init__(self, patient: Patient, last_visit_date: str, complaints: str) -> None:
        self._patient: Patient = patient
        self._last_visit_date: str = last_visit_date
        self._complaints: str = complaints
    
    def display(self) -> str:
        """Реализация метода display() для Protocol Displayable"""
        return (f"📋 Медкарта: {self._patient.full_name} | "
                f"Последний визит: {self._last_visit_date} | "
                f"Жалобы: {self._complaints[:30]}...")
    
    def __str__(self) -> str:
        return self.display()


class Prescription:
    """Рецепт (для демонстрации Displayable)"""
    def __init__(self, patient_name: str, medication: str, dosage: str) -> None:
        self._patient_name: str = patient_name
        self._medication: str = medication
        self._dosage: str = dosage
    
    def display(self) -> str:
        """Реализация метода display() для Protocol Displayable"""
        return f"💊 Рецепт: {self._patient_name} | {self._medication} | {self._dosage}"
    
    def __str__(self) -> str:
        return self.display()


class LabResult:
    """Результат лабораторного анализа (для демонстрации Scorable)"""
    def __init__(self, patient_name: str, test_name: str, value: float, normal_range: str) -> None:
        self._patient_name: str = patient_name
        self._test_name: str = test_name
        self._value: float = value
        self._normal_range: str = normal_range
    
    def score(self) -> float:
        """
        Возвращает отклонение от нормы в процентах
        Чем больше отклонение, тем хуже результат
        """
        # Для простоты считаем, что норма - это диапазон 0-100
        if self._value < 0:
            return abs(self._value)
        if self._value > 100:
            return self._value - 100
        return 0.0
    
    def display(self) -> str:
        return f"🔬 {self._test_name}: {self._patient_name} = {self._value} (норма: {self._normal_range})"
    
    def __str__(self) -> str:
        return self.display()


class HealthScore:
    """Оценка здоровья пациента (для демонстрации Scorable)"""
    def __init__(self, patient: Patient, score_value: float) -> None:
        self._patient: Patient = patient
        self._score_value: float = score_value
    
    def score(self) -> float:
        """Вернуть числовую оценку здоровья (0-100)"""
        return self._score_value
    
    def display(self) -> str:
        status = "✅ Здоров" if self._score_value >= 70 else "⚠️ Требует внимания"
        return f"🏥 {self._patient.full_name}: {self._score_value}/100 - {status}"
    
    def __str__(self) -> str:
        return self.display()


# ============ ФУНКЦИИ ДЛЯ MAP ============

def get_patient_name(patient: Patient) -> str:
    """Вернуть имя пациента"""
    return patient.full_name


def get_patient_temperature(patient: Patient) -> float:
    """Вернуть температуру пациента"""
    return patient.temperature


def get_patient_age(patient: Patient) -> int:
    """Вернуть возраст пациента"""
    return patient.age


def get_deviation_from_normal(lab_result: LabResult) -> float:
    """Вернуть отклонение от нормы"""
    return lab_result.score()


# ============ СЦЕНАРИИ ДЕМОНСТРАЦИИ ============

def scenario_3_basic_generics():
    """Сценарий 1 (задание на 3): базовая generic-коллекция с пациентами"""
    print("\n" + "=" * 80)
    print("СЦЕНАРИЙ 1 (задание на 3): TypedCollection с пациентами")
    print("=" * 80)
    
    # Создаем пациентов - используем правильные форматы групп крови
    # В валидаторе: "0+" (ноль), "A+", "B-", "AB+" и т.д.
    patient1 = Patient("Иванов Иван Иванович", 30, "A+", "Грипп", 36.6)
    patient2 = Patient("Петрова Анна Сергеевна", 25, "B-", "Ангина", 37.8)
    patient3 = Patient("Сидоров Петр Алексеевич", 45, "0+", "Перелом", 36.4)  # "0+" вместо "O+"
    patient4 = Patient("Козлова Мария Дмитриевна", 35, "AB+", "Бронхит", 38.2)
    patient5 = Patient("Новиков Алексей Викторович", 28, "A-", "Грипп", 36.9)
    
    # Создаем типизированную коллекцию
    patients_collection: TypedCollection[Patient] = TypedCollection()
    
    # Добавляем пациентов
    print("\n--- Добавление пациентов ---")
    patients_collection.add(patient1)
    patients_collection.add(patient2)
    patients_collection.add(patient3)
    
    # Проверяем длину
    print(f"\n--- Проверка длины ---")
    print(f"Количество пациентов: {len(patients_collection)}")
    
    # Получаем всех пациентов
    print(f"\n--- Все пациенты ---")
    all_patients = patients_collection.get_all()
    for i, patient in enumerate(all_patients, 1):
        print(f"{i}. {patient.full_name} - {patient.diagnosis}, {patient.temperature}°C, гр.крови: {patient.blood_type}")
    
    # Демонстрация валидации типов (попытка добавить не Patient)
    print(f"\n--- Валидация типов ---")
    print("Попытка добавить строку вместо Patient:")
    try:
        patients_collection.add("not a patient")  # type: ignore
    except Exception as e:
        print(f"  Ошибка: {e}")
    
    # Вывод всей коллекции
    print(patients_collection)


def scenario_4_generics_with_methods():
    """Сценарий 2 (задание на 4): find, filter, map"""
    print("\n" + "=" * 80)
    print("СЦЕНАРИЙ 2 (задание на 4): find, filter, map с пациентами")
    print("=" * 80)
    
    # Создаем пациентов - используем правильные группы крови
    patients = [
        Patient("Иванов Иван Иванович", 30, "A+", "Грипп", 36.6),
        Patient("Петрова Анна Сергеевна", 25, "B-", "Ангина", 37.8),
        Patient("Сидоров Петр Алексеевич", 45, "0+", "Перелом", 36.4),
        Patient("Козлова Мария Дмитриевна", 35, "AB+", "Бронхит", 38.2),
        Patient("Новиков Алексей Викторович", 28, "A-", "Грипп", 36.9)
    ]
    
    collection: TypedCollection[Patient] = TypedCollection()
    for p in patients:
        collection.add(p)
    
    # Демонстрация find()
    print("\n--- find() - поиск по условию ---")
    
    # Находим пациента с гриппом
    flu_patient = collection.find(lambda p: p.diagnosis == "Грипп")
    if flu_patient:
        print(f"  Найден пациент с гриппом: {flu_patient.full_name}")
    
    # Находим пациента с высокой температурой
    high_fever = collection.find(lambda p: p.temperature >= 38.0)
    if high_fever:
        print(f"  Найден пациент с температурой >=38°C: {high_fever.full_name} ({high_fever.temperature}°C)")
    
    # Поиск несуществующего пациента
    old_patient = collection.find(lambda p: p.age > 100)
    if old_patient is None:
        print("  Пациент старше 100 лет не найден (вернулся None)")
    
    # Демонстрация filter()
    print("\n--- filter() - фильтрация по условию ---")
    
    fever_patients = collection.filter(lambda p: p.has_fever())
    print(f"  Пациенты с температурой (>={Patient.MIN_TEMP_FOR_FEVER}°C): {len(fever_patients)}")
    for p in fever_patients:
        print(f"    - {p.full_name}: {p.temperature}°C")
    
    young_patients = collection.filter(lambda p: p.age < 30)
    print(f"\n  Пациенты младше 30 лет: {len(young_patients)}")
    for p in young_patients:
        print(f"    - {p.full_name}: {p.age} лет")
    
    # Демонстрация map() - изменение типа результата
    print("\n--- map() - преобразование с изменением типа ---")
    
    # map: Patient -> str (имена)
    names = collection.map(lambda p: p.full_name)
    print(f"  Список имен (тип list[str]): {names}")
    
    # map: Patient -> float (температура)
    temps = collection.map(lambda p: p.temperature)
    print(f"  Список температур (тип list[float]): {temps}")
    
    # map: Patient -> int (возраст)
    ages = collection.map(lambda p: p.age)
    print(f"  Список возрастов (тип list[int]): {ages}")
    
    # Демонстрация что map действительно меняет тип
    print("\n--- Проверка типов результатов map ---")
    if names:
        print(f"  type(names[0]): {type(names[0])}")
    if temps:
        print(f"  type(temps[0]): {type(temps[0])}")
    if ages:
        print(f"  type(ages[0]): {type(ages[0])}")


def scenario_5_protocols():
    """Сценарий 3 (задание на 5): Protocol и bound TypeVar в медицинской системе"""
    print("\n" + "=" * 80)
    print("СЦЕНАРИЙ 3 (задание на 5): Protocol Displayable и Scorable в медицине")
    print("=" * 80)
    
    # ===== СЦЕНАРИЙ 3A: Displayable коллекция =====
    print("\n--- Сценарий 3A: TypedCollection[D] с Displayable мед.объектами ---")
    
    # Создаем пациентов с правильными группами крови
    patient1 = Patient("Иванов Иван Иванович", 30, "A+", "Грипп", 36.6)
    patient2 = Patient("Петрова Анна Сергеевна", 25, "B-", "Ангина", 37.5)
    
    # Создаем медицинские объекты, у которых есть метод display()
    med_record = MedicalRecord(patient1, "15.05.2026", "Кашель, головная боль, температура")
    prescription = Prescription(patient2.full_name, "Амоксициллин", "500 мг 3 раза в день")
    
    # Создаем класс-адаптер для Patient (чтобы добавить display)
    class DisplayablePatient(Patient):
        def display(self) -> str:
            status = "🌡️" if self.has_fever() else "✅"
            return f"{status} Пациент: {self.full_name}, {self.age} лет, {self.diagnosis}, {self.temperature}°C"
    
    displayable_patient = DisplayablePatient("Сидоров Петр Алексеевич", 45, "0+", "Перелом", 36.4)
    
    # Создаем типизированную коллекцию с ограничением Displayable
    displayable_collection: TypedCollection[D] = TypedCollection()
    
    # Добавляем объекты разных медицинских типов
    print("Добавление объектов в Displayable коллекцию:")
    displayable_collection.add(med_record)
    displayable_collection.add(prescription)
    displayable_collection.add(displayable_patient)
    
    # Вызов метода display() для каждого элемента (безопасно, т.к. bound гарантирует наличие)
    print("\nВызов display() для всех элементов коллекции:")
    for item in displayable_collection.get_all():
        print(f"  {item.display()}")
    
    # ===== СЦЕНАРИЙ 3B: Scorable коллекция =====
    print("\n--- Сценарий 3B: TypedCollection[S] с Scorable мед.объектами ---")
    
    # Создаем медицинские объекты, у которых есть метод score()
    lab_result1 = LabResult("Иванов И.И.", "Общий анализ крови", 120, "90-110")
    lab_result2 = LabResult("Петрова А.С.", "Глюкоза", 6.5, "3.5-5.5")
    lab_result3 = LabResult("Сидоров П.А.", "Холестерин", 180, "<200")
    
    health_score1 = HealthScore(patient1, 85.0)
    health_score2 = HealthScore(patient2, 62.0)
    
    # Создаем типизированную коллекцию с ограничением Scorable
    scorable_collection: TypedCollection[S] = TypedCollection()
    
    # Добавляем объекты разных типов
    print("Добавление объектов в Scorable коллекцию:")
    scorable_collection.add(lab_result1)
    scorable_collection.add(lab_result2)
    scorable_collection.add(lab_result3)
    scorable_collection.add(health_score1)
    scorable_collection.add(health_score2)
    
    # Вызов метода score() для всех элементов (безопасно)
    print("\nВызов score() для всех элементов коллекции:")
    for item in scorable_collection.get_all():
        s = item.score()
        print(f"  {item.display()} -> score: {s}")
    
    # ===== Дополнительная демонстрация: find/filter/map с Scorable коллекцией =====
    print("\n--- Дополнительно: find/filter/map с Scorable коллекцией ---")
    
    # Поиск лабораторного результата с высоким отклонением
    high_deviation = scorable_collection.find(lambda x: x.score() > 10)
    if high_deviation:
        print(f"  Найден результат с отклонением >10: {high_deviation.display()}")
    
    # Фильтрация - только лабораторные результаты
    lab_results_only = scorable_collection.filter(lambda x: isinstance(x, LabResult))
    print(f"\n  Только лабораторные результаты ({len(lab_results_only)} шт.):")
    for item in lab_results_only:
        print(f"    - отклонение: {item.score():.1f}")
    
    # map - получение списка score'ов
    scores = scorable_collection.map(lambda x: x.score())
    print(f"\n  Список всех score'ов: {scores}")
    
    # map с преобразованием типа - получаем список строк
    score_statuses = scorable_collection.map(lambda x: f"Score: {x.score():.1f}")
    print(f"  Статусы (list[str]): {score_statuses}")


# ============ MAIN ============

def main():
    """Главная функция демонстрации"""
    print("\n" + "=" * 80)
    print("ЛАБОРАТОРНАЯ РАБОТА №6 - ДЕМОНСТРАЦИЯ")
    print("Тема: Generics, Typing, Protocols в медицинской системе")
    print("=" * 80)
    
    # Задание на 3
    scenario_3_basic_generics()
    
    # Задание на 4
    scenario_4_generics_with_methods()
    
    # Задание на 5
    scenario_5_protocols()
    
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 80)


if __name__ == "__main__":
    main()