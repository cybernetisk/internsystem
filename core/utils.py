from core.models import Semester
from datetime import datetime
from rest_framework.routers import SimpleRouter, DefaultRouter
import math


def get_semester(semester_offset=0):
    """Get the Semester-object relative to this semester. Create it if needed."""
    now = datetime.now()
    year = now.year
    sem = int(math.ceil(now.month / 6.0))  # returns 1 or 2

    # calculate correct year and sem from offset
    if semester_offset != 0:
        sem += semester_offset - 1

        year += sem / 2
        sem = (sem % 2) + 1

    sem = Semester.SPRING if sem == 1 else Semester.FALL

    obj, created = Semester.objects.get_or_create(year=year, semester=sem)

    return obj


def get_semester_details_from_date(date):
    """Get year and semester details, but not a real semester object."""
    return {
        'year': date.year,
        'semester': Semester.FALL if date.month > 6 else Semester.SPRING
    }


def get_semester_of_date(date):
    """Get the Semester-object of a specific date. Create it if needed."""
    details = get_semester_details_from_date(date)
    return Semester.objects.get_or_create(year=details['year'], semester=details['semester'])[0]


class SharedAPIRootRouter(SimpleRouter):
    """Shared API-router to maintain a shared DefaultRouter for application urls"""
    shared_router = DefaultRouter(trailing_slash=False)

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)
        super().register(*args, **kwargs)
