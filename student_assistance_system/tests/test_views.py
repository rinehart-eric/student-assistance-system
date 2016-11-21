from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import RequestFactory
from autofixture import AutoFixture
from student_assistance_system.models import *
from student_assistance_system import views


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

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
        url = reverse("student_assistance_system:edit_schedule", kwargs={'schedule_id': 3})
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/view_schedule.html')
        view = self.client.get(url,follow = True)
        self.client.logout()


class SearchViewTestCase(LoginTestCase):
    def test_search_authorized(self):
        self.validate_login()
        url = reverse("student_assistance_system:search")
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/search.html')
        self.client.logout()

    def test_search_unauthorized(self):
        url = reverse("student_assistance_system:search")
        self.validate_response(self.client.get(url), expected_status_code=302)
        self.validate_response(self.client.get(url, follow=True), expected_template_name='registration/login.html')


class SearchResultsViewTestCase(LoginTestCase):
    def test_search_results_authorized(self):
        self.validate_login()
        url = reverse("student_assistance_system:courses")
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/search_results.html')
        self.client.logout()

    def test_search_unauthorized(self):
        url = reverse("student_assistance_system:courses")
        self.validate_response(self.client.get(url), expected_status_code=302)
        self.validate_response(self.client.get(url, follow=True), expected_template_name='registration/login.html')

    def test_search_name(self):
        view = views.SearchResultsView(template_name='student_assistance_system/search_results.html')
        course1 = AutoFixture(Course, generate_fk=True, field_values=dict(name='Intro to Composition')).create_one()
        course2 = AutoFixture(Course, generate_fk=True, field_values=dict(name='Calculus I')).create_one()
        course3 = AutoFixture(Course, generate_fk=True, field_values=dict(name='Spanish I')).create_one()
        section = AutoFixture(Section, generate_m2m=False, field_values=dict(course=course1)).create_one()
        AutoFixture(Section, generate_m2m=False, field_values=dict(course=course2)).create_one()
        AutoFixture(Section, generate_m2m=False, field_values=dict(course=course3)).create_one()
        sections = Section.objects.all()
        self.assertEqual(list(view.filter_by_name({"name": "Intro to Composition"}, sections)), [section])

    def test_search_number(self):
        view = views.SearchResultsView(template_name='student_assistance_system/search_results.html')
        course1 = AutoFixture(Course, generate_fk=True, field_values=dict(course_number='102')).create_one()
        course2 = AutoFixture(Course, generate_fk=True, field_values=dict(course_number='103')).create_one()
        course3 = AutoFixture(Course, generate_fk=True, field_values=dict(course_number='104')).create_one()
        section = AutoFixture(Section, generate_m2m=False, field_values=dict(course=course1)).create_one()
        AutoFixture(Section, generate_m2m=False, field_values=dict(course=course2)).create_one()
        AutoFixture(Section, generate_m2m=False, field_values=dict(course=course3)).create_one()
        sections = Section.objects.all()
        self.assertEqual(list(view.filter_by_course_number({"num1": "102"}, sections)), [section])

    def test_search_department(self):
        view = views.SearchResultsView(template_name='student_assistance_system/search_results.html')
        dept1 = AutoFixture(Department, generate_fk=True, field_values=dict(abbr_name='EECS')).create_one()
        dept2 = AutoFixture(Department, generate_fk=True, field_values=dict(abbr_name='MATH')).create_one()
        course1 = AutoFixture(Course, generate_fk=True, field_values=dict(department=dept1)).create_one()
        course2 = AutoFixture(Course, generate_fk=True, field_values=dict(department=dept2)).create_one()
        section = AutoFixture(Section, generate_m2m=False, field_values=dict(course=course1)).create_one()
        AutoFixture(Section, generate_m2m=False, field_values=dict(course=course2)).create_one()
        sections = Section.objects.all()
        self.assertEqual(list(view.filter_by_department({"dep": "EECS"}, sections)), [section])

    def test_search_professor(self):
        view = views.SearchResultsView(template_name='student_assistance_system/search_results.html')
        course = AutoFixture(Course, generate_fk=True, field_values=dict(credit_hours=4)).create_one()
        section = AutoFixture(Section, generate_m2m=False, field_values=dict(course=course, professor="James Howard")).create_one()
        AutoFixture(Section, generate_m2m=False, field_values=dict(course=course, professor="Ed Sullivan")).create_one()
        section2 = AutoFixture(Section, generate_m2m=False, field_values=dict(course=course, professor="James Howard")).create_one()
        sections = Section.objects.all()
        self.assertEqual(list(view.filter_by_professor({"prof": "James Howard"}, sections)), [section, section2])
