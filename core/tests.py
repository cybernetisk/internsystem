from django.test import TestCase


class FixturesTestCase(TestCase):
    fixtures = ['nfccard', 'semester', 'user']

    def test_core_fixtures(self):
        return True
