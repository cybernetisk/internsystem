from core.models import Semester
from datetime import datetime
import math

"""Get the Semester-object relative to this semester. Create it if needed."""
def get_semester(semester_offset=0):
    now = datetime.now()
    year = now.year
    sem = int(math.ceil(now.month/6.0))  # returns 1 or 2

    # calculate correct year and sem from offset
    if semester_offset != 0:
        sem += semester_offset - 1

        year += sem / 2
        sem = (sem % 2) + 1

    sem = Semester.SPRING if sem == 1 else Semester.FALL

    obj, created = Semester.objects.get_or_create(year=year, semester=sem)

    return obj
