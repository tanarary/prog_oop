"""
ЛР-5: Демонстрация функций высшего порядка, стратегий и цепочек операций
"""

from base import Patient
from models import EmergencyPatient
from models import ChronicPatient
from collection import PatientRegistry
import strategies as st


def create_test_patients() -> PatientRegistry:
    """Создание тестовой коллекции пациентов"""
    registry = PatientRegistry()
    
    # Обычные пациенты - используйте корректные группы крови согласно вашему валидатору
    # Из ошибки видно, что допустимые значения: 1, 2, 3, 4, A+, A-, B+, B-, AB+, AB-, 0+, 0-, не указана
    registry.add(Patient("Иванов Иван Иванович", 45, "A+", "Гипертония", 36.8))
    registry.add(Patient("Петрова Мария Сергеевна", 28, "0+", "ОРВИ", 38.2))  # 0+ а не O+
    registry.add(Patient("Сидоров Алексей Петрович", 62, "B-", "Гастрит", 36.5))
    
    # Экстренные пациенты
    registry.add(EmergencyPatient("Кузнецова Анна Владимировна", 34, "A-", 
                                   "Аппендицит", 4, 38.5))
    registry.add(EmergencyPatient("Морозов Дмитрий Игоревич", 68, "0+", 
                                   "Инфаркт", 5, 37.8))
    
    # Хронические пациенты
    registry.add(ChronicPatient("Васильева Елена Павловна", 58, "B+", 
                                 "Сахарный диабет", "Сахарный диабет 2 типа", 12, 36.9))
    registry.add(ChronicPatient("Николаев Сергей Андреевич", 52, "AB+", 
                                 "Бронхиальная астма", "Бронхиальная астма", 8, 37.5))
    
    return registry


def scenario1_sorted_with_key():
    """
    Сценарий 1: Сортировка с параметром key=
    """
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 1: Сортировка с параметром key=")
    print("="*70)
    
    registry = create_test_patients()
    patients_list = registry.get_all()
    
    print("\n1.1 Сортировка по ФИО (по алфавиту):")
    print("-" * 50)
    sorted_by_name = sorted(patients_list, key=st.by_full_name)
    for p in sorted_by_name:
        print(f"   {p.full_name:35} | {p.age} лет")
    
    print("\n1.2 Сортировка по температуре (от высокой к низкой):")
    print("-" * 50)
    sorted_by_temp = sorted(patients_list, key=st.by_temperature, reverse=True)
    for p in sorted_by_temp:
        print(f"   {p.full_name:35} | {p.temperature}°C")
    
    print("\n1.3 Сортировка по нескольким критериям:")
    print("-" * 50)
    sorted_by_multi = sorted(patients_list, key=st.by_multiple_criteria)
    for p in sorted_by_multi:
        status_mark = "🏥" if p.status == "на лечении" else "📤"
        print(f"   {status_mark} {p.full_name:30} | {p.status:10} | {p.temperature}°C")


def scenario2_filter():
    """Сценарий 2: Фильтрация с filter()"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 2: Фильтрация с filter()")
    print("="*70)
    
    registry = create_test_patients()
    
    print("\n2.1 Фильтр: только экстренные пациенты")
    print("-" * 50)
    emergency_patients = list(filter(st.is_emergency, registry.get_all()))
    for p in emergency_patients:
        print(f"   {p.full_name} | Тяжесть: {p.severity}/5")
    
    print("\n2.2 Фильтр: критические пациенты")
    print("-" * 50)
    critical_patients = list(filter(st.is_critical, registry.get_all()))
    for p in critical_patients:
        print(f"   {p.full_name} | {p.temperature}°C")
    
    print("\n2.3 Фильтр: пациенты с нормальной температурой")
    print("-" * 50)
    normal_temp_filter = st.make_temperature_filter(36.0, 36.9)
    normal_temp_patients = list(filter(normal_temp_filter, registry.get_all()))
    for p in normal_temp_patients:
        print(f"   {p.full_name} | {p.temperature}°C")


def scenario3_map():
    """Сценарий 3: Преобразование с map()"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 3: Преобразование с map()")
    print("="*70)
    
    registry = create_test_patients()
    
    print("\n3.1 Преобразование в краткие строки:")
    print("-" * 50)
    short_strings = list(map(st.to_short_string, registry.get_all()))
    for s in short_strings:
        print(f"   {s}")
    
    print("\n3.2 Извлечение возрастов:")
    print("-" * 50)
    ages = list(map(lambda p: p.age, registry.get_all()))
    print(f"   Возраста: {ages}")
    print(f"   Средний возраст: {sum(ages)/len(ages):.1f} лет")
    
    print("\n3.3 Преобразование в словари:")
    print("-" * 50)
    dicts = list(map(st.to_info_dict, registry.get_all()))
    for d in dicts[:3]:
        print(f"   {d}")


def scenario4_chain_operations():
    """Сценарий 4: Цепочка операций"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 4: Цепочка операций filter → sort → apply")
    print("="*70)
    
    registry = create_test_patients()
    
    print("\nНачальная коллекция:")
    print(registry)
    
    print("\nЦепочка: фильтр(активные) → сортировка(по температуре) → apply(отметить осмотр)")
    print("-" * 50)
    
    result = (registry
              .filter_by(st.is_active)
              .sort_by(st.by_temperature, reverse=True)
              .apply(st.mark_as_visited))
    
    print("\nРезультат:")
    print(result)


def scenario5_strategy_pattern():
    """Сценарий 5: Паттерн Стратегия"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 5: Паттерн Стратегия (callable-объекты)")
    print("="*70)
    
    registry = create_test_patients()
    
    strategies = [
        st.SortByNameStrategy(),
        st.SortByAgeStrategy(),
        st.SortByPriorityStrategy()
    ]
    
    for strategy in strategies:
        print(f"\n{str(strategy)}:")
        print("-" * 50)
        
        temp_registry = PatientRegistry()
        for p in registry.get_all():
            temp_registry.add(p)
        
        temp_registry.sort_by(strategy)
        for p in temp_registry.get_all()[:3]:
            if isinstance(p, EmergencyPatient):
                type_mark = "🚑"
            elif isinstance(p, ChronicPatient):
                type_mark = "📋"
            else:
                type_mark = "👤"
            print(f"   {type_mark} {p.full_name:35} | Возраст: {p.age} | Темп: {p.temperature}°C")


def scenario6_lambda_vs_named():
    """Сценарий 6: Lambda vs именованная функция"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 6: Lambda vs именованная функция")
    print("="*70)
    
    registry = create_test_patients()
    
    print("\n6.1 Сортировка по возрасту:")
    print("-" * 50)
    
    print("С использованием lambda:")
    sorted_lambda = sorted(registry.get_all(), key=lambda p: p.age)
    for p in sorted_lambda[:3]:
        print(f"   {p.full_name}: {p.age} лет")
    
    print("\nС использованием именованной функции 'by_age':")
    sorted_named = sorted(registry.get_all(), key=st.by_age)
    for p in sorted_named[:3]:
        print(f"   {p.full_name}: {p.age} лет")
    
    print("\n6.2 Фильтр по возрасту (фабрика vs лямбда):")
    print("-" * 50)
    
    middle_age_filter = st.make_age_filter(30, 60)
    middle_age = list(filter(middle_age_filter, registry.get_all()))
    print(f"Через фабрику (30-60 лет): {len(middle_age)} пациентов")
    
    middle_age_lambda = list(filter(lambda p: 30 <= p.age <= 60, registry.get_all()))
    print(f"Через lambda (30-60 лет): {len(middle_age_lambda)} пациентов")
    
    # Сравниваем списки по ID пациентов (так как объекты нельзя хэшировать)
    ids_via_factory = [p.patient_id for p in middle_age]
    ids_via_lambda = [p.patient_id for p in middle_age_lambda]
    
    print(f"\nРезультаты совпадают: {ids_via_factory == ids_via_lambda}")
    
    # Дополнительно покажем, кто попал в фильтр
    print("\nПациенты в возрасте 30-60 лет:")
    for p in middle_age:
        print(f"   {p.full_name:35} | {p.age} лет | {p.diagnosis}")


def main():
    """Главная функция"""
    print("\n" + "="*70)
    print("ЛАБОРАТОРНАЯ РАБОТА №5".center(70))
    print("Функции как аргументы. Стратегии и делегаты".center(70))
    print("="*70)
    
    scenario1_sorted_with_key()
    scenario2_filter()
    scenario3_map()
    scenario4_chain_operations()
    scenario5_strategy_pattern()
    scenario6_lambda_vs_named()
    
    print("\n" + "="*70)
    print("Демонстрация завершена!".center(70))
    print("="*70)


if __name__ == "__main__":
    main()