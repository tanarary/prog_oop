# demo.py
from model import Patient
from collection import PatientRegistry
from datetime import datetime


def print_header(title: str):
    """Красивый заголовок"""
    print("\n" + "█"*70)
    print(f"█ {title}")
    print("█"*70)


def print_subheader(title: str):
    """Подзаголовок"""
    print("\n" + "─"*70)
    print(f"▶ {title}")
    print("─"*70)


def main():
    """Главная демонстрация"""
    
    print_header("РЕГИСТРАТУРА БОЛЬНИЦЫ - ДЕМОНСТРАЦИЯ РАБОТЫ КОЛЛЕКЦИИ")
    
    # ============ СОЗДАНИЕ ПАЦИЕНТОВ ============
    print_subheader("СОЗДАНИЕ ПАЦИЕНТОВ")
    
    patients = [
        Patient("Иванов Иван Петрович", 35, "A+", "Острый бронхит", 38.5),
        Patient("Петрова Мария Сергеевна", 28, "B-", "Ангина", 39.2),
        Patient("Сидоров Алексей Владимирович", 45, "1", "Гипертония", 36.6),
        Patient("Козлова Елена Викторовна", 30, "AB+", "Грипп", 38.9),
        Patient("Михайлов Дмитрий Олегович", 52, "B+", "Пневмония", 38.2),
        Patient("Антонова Анна Ивановна", 24, "A-", "ОРВИ", 37.5),
        Patient("Николаев Николай Петрович", 67, "2", "ХОБЛ", 36.8),
        Patient("Смирнова Ольга Владимировна", 41, "AB-", "Бронхит", 37.8),
    ]
    
    # ============ ЗАДАНИЕ 3 ============
    print_header("ЗАДАНИЕ 3: БАЗОВЫЕ ОПЕРАЦИИ")
    
    registry = PatientRegistry()
    print("Создан пустой реестр пациентов")
    
    print_subheader("1. ДОБАВЛЕНИЕ ПАЦИЕНТОВ (add)")
    for patient in patients[:4]:  # Добавляем первых 4
        registry.add(patient)
    
    print(f"\n📊 Размер коллекции: {len(registry)}")
    registry.print_all()
    
    print_subheader("2. ПОПЫТКА ДОБАВИТЬ ДУБЛИКАТ")
    try:
        registry.add(patients[0])  # Тот же пациент
    except ValueError as e:
        print(f"❌ Ошибка (ожидаемо): {e}")
    
    print_subheader("3. ПОПЫТКА ДОБАВИТЬ НЕПРАВИЛЬНЫЙ ТИП")
    try:
        registry.add("Это строка, а не пациент")
    except TypeError as e:
        print(f"❌ Ошибка (ожидаемо): {e}")
    
    print_subheader("4. УДАЛЕНИЕ ПАЦИЕНТА (remove)")
    registry.remove(patients[1])  # Удаляем Петрову
    print(f"\n📊 После удаления: {len(registry)} пациентов")
    registry.print_all()
    
    print_subheader("5. ПОЛУЧЕНИЕ ВСЕХ ПАЦИЕНТОВ (get_all)")
    all_patients = registry.get_all()
    print(f"Получено {len(all_patients)} пациентов через get_all():")
    for p in all_patients:
        print(f"   - {p.full_name}")
    
    # ============ ЗАДАНИЕ 4 ============
    print_header("ЗАДАНИЕ 4: ПОИСК И СПЕЦИАЛЬНЫЕ МЕТОДЫ")
    
    # Добавим остальных пациентов
    for patient in patients[4:7]:
        registry.add(patient)
    
    print_subheader("1. ПОИСК ПО ID (find_by_id)")
    registry.find_by_id(1)
    registry.find_by_id(99)
    
    print_subheader("2. ПОИСК ПО ИМЕНИ (find_by_name)")
    registry.find_by_name("Иван")
    registry.find_by_name("Анна")
    
    
    print_subheader("3. ДЕМОНСТРАЦИЯ __len__")
    print(f"Количество пациентов в реестре: {len(registry)}")
    
    print_subheader("4. ДЕМОНСТРАЦИЯ __iter__ (for item in collection)")
    print("Перебираем всех пациентов:")
    for i, patient in enumerate(registry, 1):
        print(f"   {i:2}. {patient.full_name:35} | {patient.diagnosis}")
    
    # ============ ЗАДАНИЕ 5 ============
    print_header("ЗАДАНИЕ 5: ИНДЕКСАЦИЯ, СОРТИРОВКА, ФИЛЬТРАЦИЯ")
    
    print_subheader("1. ДЕМОНСТРАЦИЯ __getitem__ (индексация)")
    print(f"Первый пациент (registry[0]): {registry[0].full_name}")
    print(f"Третий пациент (registry[2]): {registry[2].full_name}")
    print(f"Последний пациент (registry[-1]): {registry[-1].full_name}")
    
    
    print_subheader("2. УДАЛЕНИЕ ПО ИНДЕКСУ (remove_at)")
    removed = registry.remove_at(2)
    print(f"Удален: {removed.full_name}")
    print(f"Осталось пациентов: {len(registry)}")
    
    print_subheader("3. СОРТИРОВКА ПО ФИО (sort_by_name)")
    registry.sort_by_name().print_all()  # Цепочка вызовов работает!
    
    
    print_subheader("3. ФИЛЬТРАЦИЯ: get_active()")
    active_registry = registry.get_active()
    active_registry.print_all()
    
    print_subheader("4. ОПЕРАТОР in")
    test_patient = patients[0]
    print(f"Пациент '{test_patient.full_name}' в реестре? {test_patient in registry}")
    
    # Создаем нового пациента для проверки
    new_patient = Patient("Тестов Тест Тестович", 50, "0+", "Тестовый диагноз", 36.6)
    print(f"Новый пациент '{new_patient.full_name}' в реестре? {new_patient in registry}")
    
    print_subheader("5. ОЧИСТКА КОЛЛЕКЦИИ")
    print(f"До очистки: {len(registry)} пациентов")
    registry.clear()
    print(f"После очистки: {len(registry)} пациентов")
    print(f"Коллекция пуста? {registry.is_empty()}")
    



if __name__ == "__main__":
    main()