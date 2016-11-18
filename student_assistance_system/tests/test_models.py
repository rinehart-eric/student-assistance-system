from autofixture import AutoFixture
from django.test import TestCase
from student_assistance_system.models import RequirementSet, Requirement


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

"""
class RequirementTest(TestCase):
    def setUp(self):
"""
