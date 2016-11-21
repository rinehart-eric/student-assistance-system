from autofixture import AutoFixture
from django.test import TestCase
from student_assistance_system.models import *
from django.contrib.auth.models import User


class RequirementSetTest(TestCase):
    def setUp(self):
        self.test_reqs = AutoFixture(RequirementSet, generate_fk=True).create_one()

    def test_requirementset_type(self):
        values = {
            0: 'Major',
            1: 'Minor',
            2: 'Concentration',
        }

        for reqs_type in values:
            self.test_reqs.type = reqs_type
            self.assertEqual(self.test_reqs.type_name(), values[reqs_type])


class RequirementTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.req_courses = AutoFixture(Course, generate_fk=True, field_values=dict(course_number='101', credit_hours=4)).create(10)
        cls.other_courses = AutoFixture(Course, generate_fk=True, field_values=dict(course_number='102')).create(5)

        req_queryset = Course.objects.filter(course_number__exact='101')
        cls.req = create_requirement('test', None, 10, req_queryset)

        cls.user = AutoFixture(User, generate_fk=True).create_one()
        cls.schedule = AutoFixture(Schedule, generate_m2m=False, field_values=dict(user=cls.user.profile)).create_one()

    def setUp(self):
        for i in range(0, 9):
            CompletedCourse.objects.create(user=self.user.profile, course=self.req_courses[i], grade='A')

    def tearDown(self):
        for cc in CompletedCourse.objects.all():
            cc.delete()
        self.req.required_hours = None
        self.req.required_courses = 10

    def test_invalid_req_types(self):
        with self.assertRaises(ValueError):
            create_requirement('test', 10, 10, Course.objects.all())
        with self.assertRaises(ValueError):
            create_requirement('test', None, None, Course.objects.all())

    def add_last_section(self):
        section = AutoFixture(Section, generate_m2m=False, field_values=dict(course=self.req_courses[9])).create_one()
        self.schedule.sections.add(section)

    def test_get_course_set(self):
        self.assertListEqual(list(self.req.get_course_set()), self.req_courses)

    def test_get_course_statuses_empty_schedule(self):
        statuses = self.req.get_course_statuses(self.user, self.schedule)
        for i in range(0, 9):
            self.assertEqual(statuses[self.req_courses[i]], 'F')
        self.assertEqual(statuses[self.req_courses[9]], 'U')

    def test_get_course_statuses_all_enrolled(self):
        self.add_last_section()
        statuses = self.req.get_course_statuses(self.user, self.schedule)
        for i in range(0, 9):
            self.assertEqual(statuses[self.req_courses[i]], 'F')
        self.assertEqual(statuses[self.req_courses[9]], 'S')

    def check_fulfillment(self, expected):
        statuses = self.req.get_course_statuses(self.user, self.schedule)
        self.assertEqual(self.req.fulfillment_status(statuses), expected)

    def test_fulfillment_status_count_unfulfilled(self):
        self.check_fulfillment('U')

    def test_fulfillment_status_count_schedule_fulfills(self):
        self.add_last_section()
        self.check_fulfillment('S')

    def test_fulfillment_status_count_fulfilled(self):
        CompletedCourse.objects.create(user=self.user.profile, course=self.req_courses[9], grade='A')
        self.check_fulfillment('F')

    def set_req_hours(self, hours):
        self.req.required_courses = None
        self.req.required_hours = hours

    def test_fulfillment_status_hours_unfulfilled(self):
        self.set_req_hours(37)
        self.check_fulfillment('U')
        self.set_req_hours(36)
        self.check_fulfillment('F')
        self.set_req_hours(35)
        self.check_fulfillment('F')

    def test_fulfillment_status_count_schedule_fulfills(self):
        self.add_last_section()
        self.set_req_hours(40)
        self.check_fulfillment('S')

class ScheduleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AutoFixture(User, generate_fk=True).create_one()
        cls.schedule = AutoFixture(Schedule, generate_m2m=False, field_values=dict(user=cls.user.profile)).create_one()
        cls.req_courses = AutoFixture(Course, generate_fk=True, field_values=dict(course_number='101', credit_hours=4)).create(10)

    def test_delete_section(self):
        section = AutoFixture(Section, generate_m2m=False, field_values=dict(course=self.req_courses[9])).create_one()
        self.schedule.sections.add(section)
        self.assertEqual(self.schedule.sections.count(), 1)
        self.schedule.delete_section(section)
        self.assertEqual(self.schedule.sections.count(), 0)