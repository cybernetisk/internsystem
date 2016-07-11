from django.test import TestCase


class FixturesTestCase(TestCase):
    fixtures = ['semester', 'user', 'members']

    def test_members_fixtures(self):
        return True
