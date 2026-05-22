import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class PatientNotFoundError(Exception):
    """Пациент не найден в коллекции."""
    pass

class DuplicatePatientError(Exception):
    """Пациент с таким ID уже существует."""
    pass

class InvalidPatientDataError(Exception):
    """Некорректные данные при создании/изменении пациента."""
    pass