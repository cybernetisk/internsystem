from django.test import TestCase


class FixturesTestCase(TestCase):
    fixtures = ['semester', 'user', 'nfccard', 'voucher']

    def test_voucher_fixtures(self):
        return True
