from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test', password='test')

    def validate_login(self):
        self.assertTrue(self.client.login(username='test', password='test'))

    def validate_response(self, response, expected_status_code=200, expected_template_name=None):
        self.assertEqual(response.status_code, expected_status_code)
        if expected_template_name:
            print(response.templates)
            self.assertIsNotNone(response.templates)
            self.assertTrue(expected_template_name in map(lambda t: t.name, response.templates))
        else:
            print(response.templates)
            self.assertFalse(response.templates)


class IndexTestCase(LoginTestCase):
    def test_index_unauthorized(self):
        url = reverse("student_assistance_system:index")
        self.validate_response(self.client.get(url), expected_status_code=302)
        self.validate_response(self.client.get(url, follow=True), expected_template_name='registration/login.html')

    def test_index_authorized(self):
        self.validate_login()

        url = reverse("student_assistance_system:index")
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/index.html')

        self.client.logout()


class ProfileTestCase(LoginTestCase):
    def test_profile_unauthorized(self):
        url = reverse("student_assistance_system:profile")
        self.validate_response(self.client.get(url), expected_status_code=302)
        self.validate_response(self.client.get(url, follow=True), expected_template_name='registration/login.html')

    def test_profile_authorized(self):
        self.validate_login()

        url = reverse("student_assistance_system:profile")
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/profile.html')

        self.client.logout()


class ViewScheduleTestCase(LoginTestCase):
    def test_schedule_authorized(self):
        self.validate_login()
        url = reverse("student_assistance_system:view_schedule", kwargs={'schedule_id': 3})
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/view_schedule.html')
        self.client.logout()

    def test_edit_schedule_authorized(self):
        self.validate_login()
        url = reverse("student_assistance_system:view_schedule", kwargs={'schedule_id': 3})
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/view_schedule.html')
        self.client.logout()