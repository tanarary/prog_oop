"""Консольный интерфейс (CLI) для управления пациентами."""
import sys
import os

# Добавляем пути для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from lab3.base import Patient
from lab3.models import EmergencyPatient
from lab3.models import ChronicPatient
from .app import PatientApp
from .exceptions import PatientNotFoundError, DuplicatePatientError, InvalidPatientDataError


class ConsoleInterface:
    """Обрабатывает ввод/вывод, меню, взаимодействие с пользователем."""

    def __init__(self, app: PatientApp):
        self.app = app

    def run(self):
        """Главный цикл приложения."""
        while True:
            self._show_menu()
            choice = self._get_choice(0, 12)
            if choice == 0:
                print("До свидания!")
                break
            elif choice == 1:
                self._add_patient()
            elif choice == 2:
                self._show_all_patients()
            elif choice == 3:
                self._find_patient_by_id()
            elif choice == 4:
                self._find_patient_by_name()
            elif choice == 5:
                self._update_diagnosis()
            elif choice == 6:
                self._remove_patient()
            elif choice == 7:
                self._filter_menu()
            elif choice == 8:
                self._sort_menu()
            elif choice == 9:
                self._show_statistics()
            elif choice == 10:
                self._discharge_patient()
            elif choice == 11:
                self._show_emergency()
            elif choice == 12:
                self._show_critical()
            input("\nНажмите Enter, чтобы продолжить...")

    def _show_menu(self):
        print("\n" + "=" * 60)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 60)
        print("1. Добавить пациента")
        print("2. Показать всех пациентов")
        print("3. Найти пациента по ID")
        print("4. Найти пациента по ФИО (часть)")
        print("5. Изменить диагноз")
        print("6. Удалить пациента")
        print("7. Фильтрация пациентов")
        print("8. Сортировка пациентов")
        print("9. Статистика")
        print("10. Выписать пациента")
        print("11. Показать только экстренных")
        print("12. Показать критических пациентов")
        print("0. Выход")

    def _get_choice(self, min_val: int, max_val: int) -> int:
        while True:
            try:
                choice = int(input("Ваш выбор: "))
                if min_val <= choice <= max_val:
                    return choice
                print(f"Пожалуйста, введите число от {min_val} до {max_val}")
            except ValueError:
                print("Ошибка: введите целое число")

    def _get_yes_no(self, prompt: str) -> bool:
        while True:
            ans = input(prompt + " (y/n): ").lower()
            if ans in ('y', 'yes', 'да'):
                return True
            if ans in ('n', 'no', 'нет'):
                return False
            print("Введите 'y' или 'n'")

    # ---------- Добавление пациента ----------
    def _add_patient(self):
        print("\n--- Добавление нового пациента ---")
        print("Тип пациента: 1 - Обычный, 2 - Экстренный, 3 - Хронический")
        type_choice = self._get_choice(1, 3)
        try:
            full_name = input("ФИО: ").strip()
            age = int(input("Возраст: "))
            blood_type = input("Группа крови (например, A+, 0+, B-): ").strip()
            diagnosis = input("Диагноз: ").strip()
            temperature = float(input("Температура тела: "))

            if type_choice == 1:
                patient = self.app.add_patient(full_name, age, blood_type, diagnosis, temperature, "base")
                print(f"✅ Обычный пациент {patient.full_name} добавлен (ID: {patient.patient_id})")
            elif type_choice == 2:
                severity = int(input("Степень тяжести (1-5): "))
                patient = self.app.add_patient(full_name, age, blood_type, diagnosis, temperature,
                                               "emergency", severity=severity)
                print(f"🚑 Экстренный пациент {patient.full_name} добавлен (ID: {patient.patient_id}, тяжесть {severity})")
            else:
                chronic_disease = input("Хроническое заболевание: ").strip()
                years = int(input("Сколько лет болеет: "))
                patient = self.app.add_patient(full_name, age, blood_type, diagnosis, temperature,
                                               "chronic", chronic_disease=chronic_disease, years_with_disease=years)
                print(f"📋 Хронический пациент {patient.full_name} добавлен (ID: {patient.patient_id})")
        except InvalidPatientDataError as e:
            print(f"❌ Ошибка данных: {e}")
        except ValueError as e:
            print(f"❌ Неверный формат: {e}")

    # ---------- Показать всех ----------
    def _show_all_patients(self):
        patients = self.app.get_all_patients()
        if not patients:
            print("Нет пациентов.")
            return
        self._print_patients_table(patients)

    # ---------- Поиск по ID ----------
    def _find_patient_by_id(self):
        try:
            pid = int(input("Введите ID пациента: "))
            patient = self.app.find_by_id(pid)
            if patient:
                print(patient)
            else:
                print(f"Пациент с ID {pid} не найден.")
        except ValueError:
            print("ID должен быть числом.")

    # ---------- Поиск по имени ----------
    def _find_patient_by_name(self):
        substr = input("Введите часть ФИО: ").strip()
        results = self.app.find_by_name(substr)
        if not results:
            print("Ничего не найдено.")
        else:
            self._print_patients_table(results)

    # ---------- Изменить диагноз ----------
    def _update_diagnosis(self):
        try:
            pid = int(input("ID пациента: "))
            new_diagnosis = input("Новый диагноз: ").strip()
            patient = self.app.update_diagnosis(pid, new_diagnosis)
            print(f"Диагноз изменён: {patient}")
        except PatientNotFoundError as e:
            print(f"❌ {e}")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

    # ---------- Удалить с подтверждением ----------
    def _remove_patient(self):
        try:
            pid = int(input("ID пациента для удаления: "))
            patient = self.app.find_by_id(pid)
            if not patient:
                print(f"Пациент с ID {pid} не найден.")
                return
            print(patient)
            if self._get_yes_no(f"Удалить пациента '{patient.full_name}'?"):
                self.app.remove_patient(pid, confirm=True)
                print(f"✅ Пациент {patient.full_name} удалён.")
        except PatientNotFoundError as e:
            print(f"❌ {e}")
        except ValueError:
            print("ID должен быть числом.")

    # ---------- Фильтрация (подменю) ----------
    def _filter_menu(self):
        print("\n--- Фильтрация пациентов ---")
        print("1. Активные (на лечении)")
        print("2. Экстренные")
        print("3. Критические (температура ≥39° или тяжесть≥4)")
        print("4. По диапазону температур")
        print("5. По диапазону возрастов")
        choice = self._get_choice(1, 5)
        try:
            if choice == 1:
                filtered = self.app.filter_active()
            elif choice == 2:
                filtered = self.app.filter_emergency()
            elif choice == 3:
                filtered = self.app.filter_critical()
            elif choice == 4:
                min_t = float(input("Мин. температура: "))
                max_t = float(input("Макс. температура: "))
                filtered = self.app.filter_by_temperature(min_t, max_t)
            else:
                min_a = int(input("Мин. возраст: "))
                max_a = int(input("Макс. возраст: "))
                filtered = self.app.filter_by_age(min_a, max_a)
            self._print_patients_table(filtered.get_all())
        except ValueError as e:
            print(f"Ошибка ввода: {e}")

    # ---------- Сортировка (подменю) ----------
    def _sort_menu(self):
        print("\n--- Сортировка пациентов ---")
        print("1. По имени (A→Я)")
        print("2. По имени (Я→A)")
        print("3. По возрасту (младшие→старшие)")
        print("4. По возрасту (старшие→младшие)")
        print("5. По температуре (от низкой к высокой)")
        print("6. По температуре (от высокой к низкой)")
        choice = self._get_choice(1, 6)
        if choice == 1:
            self.app.sort_by_name(reverse=False)
        elif choice == 2:
            self.app.sort_by_name(reverse=True)
        elif choice == 3:
            self.app.sort_by_age(reverse=False)
        elif choice == 4:
            self.app.sort_by_age(reverse=True)
        elif choice == 5:
            self.app.sort_by_temperature(reverse=False)
        else:
            self.app.sort_by_temperature(reverse=True)
        print("✅ Коллекция отсортирована.")
        self._show_all_patients()

    # ---------- Статистика ----------
    def _show_statistics(self):
        total = self.app.count()
        active = len(self.app.filter_active().get_all())
        emergency = len(self.app.filter_emergency().get_all())
        print(f"\n📊 Статистика:")
        print(f"   Всего пациентов: {total}")
        print(f"   На лечении: {active}")
        print(f"   Экстренных: {emergency}")

    # ---------- Выписать пациента ----------
    def _discharge_patient(self):
        try:
            pid = int(input("ID пациента для выписки: "))
            patient = self.app.find_by_id(pid)
            if not patient:
                print("Пациент не найден.")
                return
            if patient.status == "выписан":
                print("Пациент уже выписан.")
                return
            if patient.has_fever():
                print("Нельзя выписать пациента с повышенной температурой!")
                return
            if self._get_yes_no(f"Выписать {patient.full_name}?"):
                patient.discharge()
                print(f"✅ Пациент {patient.full_name} выписан.")
        except ValueError:
            print("ID должен быть числом.")

    # ---------- Показать экстренных ----------
    def _show_emergency(self):
        filtered = self.app.filter_emergency()
        self._print_patients_table(filtered.get_all())

    # ---------- Показать критических ----------
    def _show_critical(self):
        filtered = self.app.filter_critical()
        self._print_patients_table(filtered.get_all())

    # ---------- Утилита форматированного вывода ----------
    def _print_patients_table(self, patients: List[Patient]):
        if not patients:
            print("Нет пациентов для отображения.")
            return
        # Заголовок
        print("\n" + "-" * 100)
        print(f"{'ID':<4} {'ФИО':<30} {'Возраст':<6} {'Диагноз':<20} {'Темп.':<6} {'Статус':<12} {'Тип'}")
        print("-" * 100)
        for p in patients:
            p_type = "Обычный"
            if isinstance(p, EmergencyPatient):
                p_type = f"🚑Экстр.{p.severity}"
            elif isinstance(p, ChronicPatient):
                p_type = "📋Хронич."
            print(f"{p.patient_id:<4} {p.full_name[:30]:<30} {p.age:<6} {p.diagnosis[:20]:<20} "
                  f"{p.temperature:<6.1f} {p.status:<12} {p_type}")
        print("-" * 100)