from django.test import TestCase

from students.models import Class, House

from students.tests.test_class_api import get_sample_programme, get_sample_school


class ModelTest(TestCase):
    """Students models tests"""

    def test_class_str(self):
        """Test the string representation of class object"""
        programme = get_sample_programme()

        clas = Class.objects.create(
            programme=programme,
            programme_division='A',
            year=1,
        )

        self.assertEquals(str(clas), clas.name)

    def test_house_str(self):
        """Test the string representation of house"""
        school = get_sample_school()
        house = House.objects.create(name='Masroor', school=school)

        self.assertEqual(str(house), house.name)
