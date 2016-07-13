from django.test import TestCase
from .models import Konto, Varetelling

class KontoTestCase(TestCase):
    def setUp(self):
        Konto.objects.create(
            innkjopskonto=4010,
            varelagerkonto=1410,
            beholdningsendringskonto=4210,
            salgskonto=3010,
            navn="Varesalg",
            gruppe="DIV")

    def test_have_konto(self):
        konto = Konto.objects.first()
        self.assertIsInstance(konto, Konto, "Konto-object exists")

    def test_name(self):
        konto = Konto.objects.first()
        self.assertEqual(str(konto), "DIV: Varesalg", "Correct string representation")


class FixturesTestCase(TestCase):
    fixtures = ['user', 'varer']

    def test_varer_fixtures(self):
        self.assertEqual(Varetelling.objects.count(), 4, "There are four inventory counts")
