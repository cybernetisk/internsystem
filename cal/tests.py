from django.test import TestCase


class FixturesTestCase(TestCase):
    fixtures = ['events']

    def test_cal_fixtures(self):
        return True
