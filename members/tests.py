from django.test import TestCase
from .models import Member


class FixturesTestCase(TestCase):
    fixtures = ['semester', 'user', 'members']

    def test_semester_fixtures(self):
        self.assertEqual(Member.objects.count(), 5, "There are five members registererd")
        self.assertEqual(Member.objects.filter(honorary=True).count(), 1, "There are one honary member")
        self.assertEqual(Member.objects.filter(lifetime=True).count(), 1, "There are one lifetime member")
