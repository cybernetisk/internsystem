from django.test import TestCase
from core.models import NfcCard, User
from core.utils import get_semester_of_date
from .models import CoffeeWallet, VoucherWallet
from datetime import date


class FixturesTestCase(TestCase):
    fixtures = ['semester', 'user', 'nfccard', 'voucher']

    def test_coffee_balance(self):
        card = NfcCard.objects.get(card_uid='3b2be5a2')
        semester = get_semester_of_date(date(year=2016, month=7, day=10))
        wallet = CoffeeWallet.objects.get(card=card, semester=semester)
        self.assertEqual(wallet.cached_balance, 4, 'Cached balance of coffee wallet is 4')

    def test_voucher_balance(self):
        user = User.objects.get(username='user2')
        semester = get_semester_of_date(date(year=2016, month=7, day=10))
        wallet = VoucherWallet.objects.get(user=user, semester=semester)
        self.assertEqual(wallet.cached_balance, 2.5, 'Cached balance of voucher wallet is 2.5')
