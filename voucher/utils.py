from datetime import datetime
from core.utils import get_semester


def get_valid_semesters():
    semesters = []
    now = datetime.now()
    if now.month == 8 or now.month == 1:
        semesters.append(get_semester(-1))
    semesters.append(get_semester())
    return semesters
