from decimal import *
from datetime import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.test import TestCase
from core.models import Semester, CybUser
from bong.models import BongWallet, BongLog

# Create your tests here.
class BongTestCase(TestCase):
    def setUp(self):
        self.now = datetime.utcnow().replace(tzinfo=utc)
        self.user = User.objects.create_user(
            username = 'barfunk',
            email = 'barfunk@cyb.no',
            password = 'top_secret'
        )
        self.user.save()
        self.issuing_user = User.objects.create_user(
            username = 'sjef',
            email = 'sjef@cyb.no',
            password = 'top_secret'
        )
        self.issuing_user.save()
        self.semester = Semester(
            date_start = self.now,
            date_end = self.now
        )
        self.semester.save()
        self.cybUser = CybUser(user=self.user)
        self.cybUser.save()
        self.sjefCybUser = CybUser(user=self.issuing_user)
        self.sjefCybUser.save()
        self.wallet = BongWallet(
            semester = self.semester,
            user = self.cybUser,
            balance = 7,
            total_assigned = 15
        )
        self.wallet.save()

    def testAssignBong(self):

        self.assertEqual(self.wallet.balance, 7)
        self.assertEqual(self.wallet.total_assigned, 15)

        log = BongLog(
            wallet = self.wallet,
            action = BongLog.ISSUED,
            date_issued = self.now,
            issuing_user = self.sjefCybUser,
            hours = '4',
            bongs = '2'
        )
        log.save()

        self.assertEqual(self.wallet.balance, 9)
        self.assertEqual(self.wallet.total_assigned, 17)
