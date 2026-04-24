
from models import Patient, PatientRegistry
from interfaces import Printable, Comparable


# ============ СЦЕНАРИЙ 1: ПРОВЕРКА ИНТЕРФЕЙСОВ ============
def scenario_1_check_interfaces():
    """Проверка, что классы реализуют интерфейсы"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 1: ПРОВЕРКА РЕАЛИЗАЦИИ ИНТЕРФЕЙСОВ")
    print("="*70)
    
    # Создаем пациента
    patient = Patient("Иванов Иван Иванович", 30, "A+", "Грипп", 36.6)
    
    # Проверка через isinstance
    print(f"\n1. Проверка isinstance(patient, Printable): {isinstance(patient, Printable)}")
    print(f"2. Проверка isinstance(patient, Comparable): {isinstance(patient, Comparable)}")
    
    # Проверка наличия методов
    print("\n3. Методы интерфейса Printable:")
    print(f"   - to_string(): {patient.to_string('short')[:50]}...")
    print(f"   - to_short_string(): {patient.to_short_string()}")
    
    print("\n4. Методы интерфейса Comparable:")
    print(f"   - get_sort_key(): {patient.get_sort_key()}")
    patient2 = Patient("Петров Петр Петрович", 25, "B-", "Ангина", 36.8)
    print(f"   - compare_to(patient2): {patient.compare_to(patient2)} (ID {patient.patient_id} vs {patient2.patient_id})")
    


# ============ СЦЕНАРИЙ 2: ИНТЕРФЕЙС КАК ТИП ============
def print_all_printable(items: list[Printable], title: str = "Вывод объектов"):
    """
    УНИВЕРСАЛЬНАЯ ФУНКЦИЯ - работает с любыми Printable объектами
    Демонстрация интерфейса как типа
    """
    print(f"\n📄 {title}:")
    print("-" * 50)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.to_string('short')}")
    print("-" * 50)


def compare_two_comparable(a: Comparable, b: Comparable) -> str:
    """Универсальная функция сравнения через интерфейс Comparable"""
    try:
        result = a.compare_to(b)
        if result < 0:
            return f"{a.get_sort_key()} < {b.get_sort_key()}"
        elif result > 0:
            return f"{a.get_sort_key()} > {b.get_sort_key()}"
        else:
            return f"{a.get_sort_key()} == {b.get_sort_key()}"
    except TypeError as e:
        return f"Ошибка сравнения: {e}"


def scenario_2_interface_as_type():
    """Интерфейс как тип - полиморфные функции"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 2: ИНТЕРФЕЙС КАК ТИП (универсальные функции)")
    print("="*70)
    
    # Создаем разных пациентов (исправлено: 0+ вместо O+)
    patients = [
        Patient("Сидорова Анна Петровна", 45, "AB+", "Гипертония", 36.5),
        Patient("Козлов Дмитрий Сергеевич", 28, "0+", "Перелом", 37.1),
        Patient("Морозова Елена Владимировна", 52, "A-", "Бронхит", 38.2),
    ]
    
    # Используем универсальную функцию print_all_printable
    print_all_printable(patients, "Список пациентов (через интерфейс Printable)")
    
    # Сравнение через Comparable
    print("\nСравнение пациентов через интерфейс Comparable:")
    print(f"  {compare_two_comparable(patients[0], patients[1])}")
    print(f"  {compare_two_comparable(patients[1], patients[2])}")
    


# ============ СЦЕНАРИЙ 3: ПОЛИМОРФИЗМ ============
def scenario_3_polymorphism():
    """Разное поведение одного интерфейса в разных контекстах"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 3: ПОЛИМОРФИЗМ ЧЕРЕЗ ИНТЕРФЕЙСЫ")
    print("="*70)
    
    # Создаем пациентов с разными состояниями (исправлены ФИО - теперь есть фамилия и имя)
    patient1 = Patient("Здоровый Петр Иванович", 25, "A+", "Профосмотр", 36.5)
    patient2 = Patient("Больной Сергей Петрович", 35, "B+", "Грипп", 38.5)
    patient3 = Patient("Выздоравливающий Алексей Владимирович", 42, "0-", "Пневмония", 36.9)
    
    # Один интерфейс Printable - разное поведение (разные форматы)
    print("\n1. Разные форматы вывода одного интерфейса Printable:")
    print(f"   Short: {patient1.to_string('short')}")
    print(f"   Default: {patient1.to_string('default')}")
    print(f"   Detailed:\n{patient1.to_string('detailed')}")
    
    # Разные объекты - разное поведение to_short_string
    print("\n2. Разные объекты - разный результат to_short_string():")
    for p in [patient1, patient2, patient3]:
        print(f"   {p.to_short_string()}")
    
    # Полиморфизм в коллекции
    print("\n3. Полиморфный вывод через единый интерфейс:")
    print_all_printable([patient1, patient2, patient3], "Все пациенты (единый интерфейс)")
    


# ============ СЦЕНАРИЙ 4: ИНТЕГРАЦИЯ С КОЛЛЕКЦИЕЙ ============
def scenario_4_collection_integration():
    """Интеграция интерфейсов с PatientRegistry"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 4: ИНТЕГРАЦИЯ ИНТЕРФЕЙСОВ С КОЛЛЕКЦИЕЙ")
    print("="*70)
    
    # Создаем реестр и наполняем
    registry = PatientRegistry()
    
    patients_data = [
        ("Артемьева Мария Игоревна", 29, "A+", "Аппендицит", 37.5),
        ("Борисов Сергей Андреевич", 67, "B-", "Диабет", 36.7),
        ("Волкова Наталья Дмитриевна", 18, "0+", "ОРВИ", 38.0),
        ("Григорьев Алексей Петрович", 54, "AB-", "Инфаркт", 36.4),
    ]
    
    for name, age, blood, diagnosis, temp in patients_data:
        registry.add(Patient(name, age, blood, diagnosis, temp))
    
    # 1. Фильтрация по интерфейсу
    print("\n1. Фильтрация объектов, реализующих Printable:")
    printable_items = registry.get_printable_items()
    print(f"   Найдено объектов Printable: {len(printable_items)} из {len(registry)}")
    
    print("\n2. Фильтрация объектов, реализующих Comparable:")
    comparable_items = registry.get_comparable_items()
    print(f"   Найдено объектов Comparable: {len(comparable_items)} из {len(registry)}")
    
    # 2. Вывод через интерфейс
    print("\n3. Вывод всех пациентов через интерфейс Printable (формат 'short'):")
    registry.print_all_via_interface("short")
    
    print("\n4. Вывод через интерфейс (формат 'detailed' для первого пациента):")
    first_patient = registry[0]
    print(first_patient.to_string("detailed"))
    


# ============ СЦЕНАРИЙ 5: АРХИТЕКТУРНОЕ ПОВЕДЕНИЕ ============
def scenario_5_architectural_behavior():
    """Сортировка через Comparable и другие архитектурные решения"""
    print("\n" + "="*70)
    print("СЦЕНАРИЙ 5: АРХИТЕКТУРНОЕ ПОВЕДЕНИЕ")
    print("="*70)
    
    # Создаем коллекцию пациентов в произвольном порядке
    registry = PatientRegistry()
    
    # Создаем пациентов (ID будут присвоены в порядке создания)
    patients_raw = [
        ("Яковлев Яков Петрович", 40, "A+", "Гастрит", 36.5),
        ("Александров Александр Иванович", 25, "B+", "Тонзиллит", 37.0),
        ("Борисов Борис Сергеевич", 35, "0+", "Отит", 36.8),
        ("Григорьев Григорий Алексеевич", 30, "AB+", "Ларингит", 36.6),
    ]
    
    for name, age, blood, diagnosis, temp in patients_raw:
        registry.add(Patient(name, age, blood, diagnosis, temp))
    
    print("\n🔴 Исходный порядок (по ID):")
    for p in registry:
        print(f"   ID {p.patient_id}: {p.full_name} (возраст: {p.age})")
    
    # 1. Сортировка через Comparable (по get_sort_key)
    print("\n1. Сортировка через интерфейс Comparable (по ФИО + возраст):")
    registry.sort_by_comparable()
    for i, p in enumerate(registry, 1):
        print(f"   {i}. {p.full_name} (возраст: {p.age}) - ключ: {p.get_sort_key()}")
    
    # 2. Обратная сортировка
    print("\n2. Сортировка через Comparable (обратный порядок):")
    registry.sort_by_comparable(reverse=True)
    for i, p in enumerate(registry, 1):
        print(f"   {i}. {p.full_name} (возраст: {p.age})")
    
    # 3. Полиморфная работа - один интерфейс, разное поведение
    print("\n3. Полиморфизм: разные строковые представления через один интерфейс:")
    for p in registry.get_printable_items()[:3]:
        print(f"   {p.to_string('short')}")
    


# ============ ГЛАВНАЯ ФУНКЦИЯ ============
def main():
    
    scenarios = [
        ("1. Проверка интерфейсов", scenario_1_check_interfaces),
        ("2. Интерфейс как тип", scenario_2_interface_as_type),
        ("3. Полиморфизм через интерфейсы", scenario_3_polymorphism),
        ("4. Интеграция с коллекцией ЛР-2", scenario_4_collection_integration),
        ("5. Архитектурное поведение", scenario_5_architectural_behavior),
    ]
    
    for name, scenario_func in scenarios:
        scenario_func()
    


if __name__ == "__main__":
    main()

