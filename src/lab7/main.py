"""Точка входа в консольное приложение."""

import sys
import os

# Добавляем пути для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab5.collection import PatientRegistry
from lab7.storage import save_registry, load_registry
from lab7.app import PatientApp
from lab7.cli import ConsoleInterface

DATA_FILE = "patients.json"  # файл сохраняется в текущей директории запуска


def main():
    # Загружаем данные
    registry = load_registry(DATA_FILE)
    app = PatientApp(registry)
    cli = ConsoleInterface(app)

    print("🏥 Добро пожаловать в систему управления пациентами Городской больницы №1 🏥")
    cli.run()

    # Сохраняем при выходе
    save_registry(registry, DATA_FILE)
    print("Данные сохранены.")


if __name__ == "__main__":
    main()