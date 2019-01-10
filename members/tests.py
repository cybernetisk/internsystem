from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from core.models import User
from .models import Member


class FixturesTestCase(TestCase):
    fixtures = ['semester', 'user', 'members']

    def test_semester_fixtures(self):
        self.assertEqual(Member.objects.count(), 5, "There are five members registererd")
        self.assertEqual(Member.objects.filter(honorary=True).count(), 1, "There are one honary member")
        self.assertEqual(Member.objects.filter(lifetime=True).count(), 1, "There are one lifetime member")


class MemberRestTestCase(APITestCase):

    new_member = {'name': 'Test Testeren', 'email': 'text@example.com', 'lifetime': False, 'gdpr_approval': True,}

    def test_add_member(self):
        url = reverse('member-members-list')
        self.login()
        response = self.client.post(url, self.new_member, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)

        member = Member.objects.get()
        self.assertEqual(member.name, self.new_member.get('name'))
        self.assertEqual(member.email, self.new_member.get('email'))
        self.assertEqual(member.lifetime, self.new_member.get('lifetime'))
        self.assertEqual(member.gdpr_approval, self.new_member.get('gdpr_approval'))

    def test_add_member_not_logged_in(self):
        url = reverse('member-members-list')
        response = self.client.post(url, self.new_member, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_member_bad_request(self):
        url = reverse('member-members-list')
        data = {'email': 'text@example.com', 'lifetime': False}
        self.login()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def login(self):
        user = User.objects.get_or_create(username='cyb', email='text@example.com', is_superuser=True)
        self.client.force_authenticate(user=user[0])
