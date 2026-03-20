
from model import Patient
from datetime import datetime, timedelta

def print_separator(title):
    """Красивый разделитель"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def main():
    """Главная функция демонстрации"""
    
    print_separator("ПОСТУПЛЕНИЕ ПАЦИЕНТОВ")
    
    # Создаем пациентов
    patient1 = Patient("Иванов Иван", 35, "A+", "Острый бронхит", 38.5)
    patient2 = Patient("Сергеев Василий", 25, "B-", "Ангина", 39.2)
    patient3 = Patient("Седых Надежда Васильевна", 45, "1", "Гипертония", 36.6)
    patient4 = Patient("Козлова Елена Викторовна", 30, "AB+", "Грипп", 38.9)
    
    print(f"\nВсего пациентов в системе: {Patient.total_patients}")
    print(f"Больница: {Patient.hospital_name}")
    

    print_separator("ИНФОРМАЦИЯ О ПАЦИЕНТАХ")
    
    print("Список пациентов:")
    for patient in [patient1, patient2, patient3, patient4]:
        print(patient)
    
    print("\n" + "-"*50)
    print("repr для разработчика:")
    print(repr(patient1))
    

    print_separator("ДОСТУП К ДАННЫМ")
    
    print(f"Пациент: {patient1.full_name}")
    print(f"Возраст: {patient1.age} лет")
    print(f"Группа крови: {patient1.blood_type}")
    print(f"Диагноз: {patient1.diagnosis}")
    print(f"Температура: {patient1.temperature}°C")
    print(f"Статус: {patient1.status}")
    print(f"Дней в больнице: {patient1.days_in_hospital}")
    

    print_separator("ИЗМЕНЕНИЕ ДАННЫХ")
    
    print("Изменяем диагноз:")
    patient1.diagnosis = "Хронический бронхит"
    
    print("\nИзмеряем температуру:")
    patient1.temperature = 37.5  # Должно предупредить о лихорадке
    patient1.temperature = 36.8
    
    # ----- Демонстрация бизнес-методов -----
    print_separator("МЕДИЦИНСКИЕ ПРОВЕРКИ")
    
    print("Проверка температуры:")
    for patient in [patient1, patient2, patient3]:
        if patient.has_fever():
            print(f"{patient.full_name}: ЛИХОРАДКА! ({patient.temperature}°C)")
        else:
            print(f"{patient.full_name}: Температура в норме ({patient.temperature}°C)")
    
    print("\nПроверка возможности донорства:")
    for patient in [patient1, patient2, patient3, patient4]:
        can, reason = patient.can_donate_blood()
        status = "МОЖЕТ" if can else "Не может"
        print(f"{patient.full_name}: {status}")
        if not can:
            print(f"   Причина: {reason}")
    
    # ----- Демонстрация изменения состояния -----
    print_separator("ИЗМЕНЕНИЕ СОСТОЯНИЯ")
    
    print("Выписываем пациента:")
    try:
        patient2.temperature = 36.6  # Сначала нормализуем температуру
        patient2.discharge()
        print(patient2)
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\nПытаемся выписать с температурой:")
    try:
        patient4.discharge()  # У patient4 температура 38.9
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\nНаправляем к специалисту:")
    patient3.refer_to_specialist("кардиологу")
    print(patient3)
    
    # ----- Демонстрация ошибок валидации -----
    print_separator("ОБРАБОТКА ОШИБОК")
    
    print("Попытка 1: некорректный возраст")
    try:
        Patient("Тест Тестов", -5, "A+", "Тест", 36.6)
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\nПопытка 2: некорректная группа крови")
    try:
        Patient("Тест Тестов", 30, "R+", "Тест", 36.6)
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\nПопытка 3: температура вне диапазона")
    try:
        patient1.temperature = 43.0
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\nПопытка 4: пустой диагноз")
    try:
        Patient("Тест Тестов", 30, "A+", "", 36.6)
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # ----- Демонстрация сравнения -----
    print_separator("СРАВНЕНИЕ ПАЦИЕНТОВ")
    
    patient5 = Patient("Иванов Иван Петрович", 35, "A+", "ОРВИ", 36.6)
    
    print(f"patient1 ID: {patient1.patient_id}")
    print(f"patient5 ID: {patient5.patient_id}")
    print(f"patient1 == patient5: {patient1 == patient5}")
    print(f"patient1 == patient1: {patient1 == patient1}")
    
    # ----- Демонстрация сортировки -----
    print_separator("СОРТИРОВКА ПО ДАТЕ ПОСТУПЛЕНИЯ")
    
    # Создаем пациента с другой датой
    patients = [patient1, patient2, patient3, patient4, patient5]
    patients.sort()  # Использует __lt__
    
    for i, p in enumerate(patients, 1):
        print(f"{i}. {p.full_name} - поступил: {p.admission_date.strftime('%H:%M:%S')}")
    
    # ----- Демонстрация атрибута класса -----
    print_separator("АТРИБУТЫ КЛАССА")
    
    print(f"Через класс: Patient.total_patients = {Patient.total_patients}")
    print(f"Через экземпляр: patient1.total_patients = {patient1.total_patients}")
    print(f"Название больницы: {Patient.hospital_name}")
    
    # ----- Итоговый список пациентов -----
    print_separator("ИТОГОВЫЙ СПИСОК ПАЦИЕНТОВ")
    
    for patient in patients:
        print(patient)

if __name__ == "__main__":
    main()