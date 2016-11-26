from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import RequestFactory
from autofixture import AutoFixture
from student_assistance_system.models import *
from student_assistance_system import views
import datetime


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
    def setup(self):
        self.view = views.SearchResultsView(template_name='student_assistance_system/search_results.html')
        math_course = AutoFixture(Course, generate_fk=True,
                                  field_values=dict(name='Calculus I', course_number='121', credit_hours=4,
                                                    department=AutoFixture(Department, generate_fk=True, field_values=dict(abbr_name='MATH')).create_one()
                                                    )).create_one()
        spanish_course = AutoFixture(Course, generate_fk=True,
                                    field_values=dict(name='Intro to Spanish', course_number='101', credit_hours=4,
                                                      department=AutoFixture(Department, generate_fk=True, field_values=dict(abbr_name='SPAN')).create_one()
                                                     )).create_one()
        eecs_cource = AutoFixture(Course, generate_fk=True,
                                  field_values=dict(name='Software Engineering', course_number='393', credit_hours=3,
                                                    department=AutoFixture(Department, generate_fk=True, field_values=dict(abbr_name='EECS')).create_one()
                                                    )).create_one()
        self.math_section =AutoFixture(Section, generate_fk=True,
                                  field_values=dict(course=math_course, professor="James Howard", meeting_times=[
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=0, start_time=datetime.time(8, 30), end_time=datetime.time(9, 20))).create_one(),
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=1, start_time=datetime.time(9, 0), end_time=datetime.time(10, 15))).create_one(),
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=2, start_time=datetime.time(8, 30), end_time=datetime.time(9, 20))).create_one(),
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=4, start_time=datetime.time(8, 30), end_time=datetime.time(9, 20))).create_one()
                                  ])).create_one()
        self.spanish_section =AutoFixture(Section, generate_fk=True,
                                  field_values=dict(course=spanish_course, professor="James Howard", meeting_times=[
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=1, start_time=datetime.time(9, 0), end_time=datetime.time(10, 15))).create_one(),
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=3, start_time=datetime.time(8, 0), end_time=datetime.time(10, 15))).create_one(),
                                  ])).create_one()
        self.eecs_section =AutoFixture(Section, generate_fk=True,
                                  field_values=dict(course=eecs_cource, professor="Andy Podgurski", meeting_times=[
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=0, start_time=datetime.time(11, 40), end_time=datetime.time(12, 30))).create_one(),
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=2, start_time=datetime.time(11, 40), end_time=datetime.time(12, 30))).create_one(),
                                    AutoFixture(MeetingTime, generate_fk=True, field_values=dict(day=4, start_time=datetime.time(11, 40), end_time=datetime.time(12, 30))).create_one()
                                  ])).create_one()
        self.sections = Section.objects.all()

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
        #self.setup()
        self.assertEqual(list(self.view.filter_by_name({"name": "Intro to Spanish"}, self.sections)), [self.spanish_section])

    def test_search_number(self):
        self.setup()
        self.assertEqual(list(self.view.filter_by_course_number({"num1": "101"}, self.sections)), [self.spanish_section])

    def test_search_department(self):
        self.setup()
        self.assertEqual(list(self.view.filter_by_department({"dep": "EECS"}, self.sections)), [self.eecs_section])

    def test_search_professor(self):
        self.setup()
        self.assertEqual(list(self.view.filter_by_professor({"prof": "James Howard"}, self.sections)), [self.math_section, self.spanish_section])

    #def test_search_meeting_times(self):



class AddSectionScheduleViewTestCase(LoginTestCase):
    def test_search_authorized(self):
        self.validate_login()
        url = reverse("student_assistance_system:add_section")
        self.validate_response(self.client.get(url, follow=True), expected_template_name='student_assistance_system/view_schedule.html')
        self.client.logout()

    def test_search_unauthorized(self):
        url = reverse("student_assistance_system:search")
        self.validate_response(self.client.get(url), expected_status_code=302)
        self.validate_response(self.client.get(url, follow=True), expected_template_name='registration/login.html')
