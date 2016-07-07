import datetime

from core.utils import get_semester


def get_valid_semesters():
    semesters = []
    now = datetime.datetime.now()
    if now.month == 7 or now.month == 8 or now.month == 1:
        semesters.append(get_semester(-1))
    semesters.append(get_semester())
    return semesters


def get_first_valid_work_log_date():
    valid = datetime.date.today().replace(day=1)

    if valid.month <= 1:
        valid = valid.replace(year=valid.year - 1)
        valid = valid.replace(month=7)
    elif valid.month <= 8:
        valid = valid.replace(month=1)
    else:
        valid = valid.replace(month=7)

    return valid
