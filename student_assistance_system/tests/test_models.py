from datetime import date
from django.test import TestCase
from student_assistance_system.models import RequirementSet, Department


class RequirementSetTest(TestCase):
    def setUp(self):
        test_dept = Department.objects.create(full_name='test', abbr_name='test')
        self.test_reqs = RequirementSet.objects.create(
            name='Test Reqs',
            department=test_dept,
            type=0,
            effective_date=date.today()
        )

    def test_requirementset_type(self):
        values = {
            0: 'Major',
            1: 'Minor',
            2: 'Concentration',
        }

        for type in values:
            self.test_reqs.type = type
            self.assertEqual(self.test_reqs.requirementset_type(), values[type])
