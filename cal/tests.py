from django.test import TestCase


class FixturesTestCase(TestCase):
    fixtures = ["event"]

    def test_cal_fixtures(self):
        return True
