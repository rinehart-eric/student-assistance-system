from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

test_username = 'test'
test_password = 'test'

class IndexTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(test_username, password=test_password)

    def test_index_unauthorized(self):
        url = reverse("student_assistance_system:index")
        resp = self.client.get(url, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.templates)
        self.assertEqual(resp.templates[0].name, 'registration/login.html')

    def test_index_authorized(self):
        self.assertTrue(self.client.login(username=test_username, password=test_password))

        url = reverse("student_assistance_system:index")
        resp = self.client.get(url, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.templates)
        self.assertEqual(resp.templates[0].name, 'student_assistance_system/index.html')

        self.client.logout()
