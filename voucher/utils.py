import datetime

from core.utils import get_semester, get_semester_of_date


def get_valid_semesters():
    semesters = []
    now = datetime.datetime.now()
    if now.month == 7 or now.month == 8 or now.month == 1:
        semesters.append(get_semester(-1))
    # Corona-exception in 2020.
    elif now.year == 2020 and now.month == 9:
        semesters.append(get_semester(-1))

    # Corona-exception in 2021
    elif now.year == 2021 and now.month in [6, 7]:
        semesters.append(get_semester_of_date(datetime.date(2020, 12, 1)))

    semesters.append(get_semester())
    return semesters


def get_first_valid_work_log_date():
    valid = datetime.date.today().replace(day=1)

    if valid.month <= 1:
        valid = valid.replace(year=valid.year - 1)
        valid = valid.replace(month=7)
    elif valid.month <= 8:
        valid = valid.replace(month=1)
    # Corona-exception in 2020.
    elif valid.year == 2020 and valid.month == 9:
        valid = valid.replace(month=1)

    # Corona-exception in 2021
    elif valid.year == 2021 and (valid.month == 6 or valid.month == 7):
        valid = valid.replace(year=2020, month=8)
    else:
        valid = valid.replace(month=7)

    return valid
