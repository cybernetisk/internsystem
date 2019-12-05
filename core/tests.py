from django.test import TestCase
from .models import NfcCard, Semester, User


class FixturesTestCase(TestCase):
    fixtures = ["nfccard", "semester", "user"]

    def test_nfccard_fixtures(self):
        card = NfcCard.objects.get(card_uid="3b2be5a2")
        self.assertIsNotNone(card, "There is a NfcCard with uid 3b2be5a2")
        self.assertEqual(
            NfcCard.objects.count(), 1, "There are ony one NfcCard registered"
        )

    def test_semester_fixtures(self):
        self.assertEqual(
            Semester.objects.count(), 6, "There are six semesters registererd"
        )

    def test_user_fixtures(self):
        user = User.objects.get(username="cyb")
        self.assertIsNone(user.last_login, "User cyb have never logged in")
        self.assertEqual(User.objects.count(), 3, "There are three users registered")
