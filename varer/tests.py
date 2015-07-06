from django.test import TestCase
from varer.models import Konto

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

    def test_more(self):
        self.assertEqual(10, 20, "Ten equals twenty")

    def test_should_fail(self):
        self.assertEqual("one", "two", "One equals two")
