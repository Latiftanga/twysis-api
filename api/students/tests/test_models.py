from django.test import TestCase

from students.models import Class, House, Guardian, Student
from students.tests.test_class_api import get_sample_programme, get_sample_school
from core.tests.faker import fake


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

    def test_guardian_str(self):
        """Test the string representation of student guardian"""
        guardian = Guardian.objects.create(
            name=fake.name(),
            relation=fake.guardian_relation(),
            address=fake.address(),
            phone='0200000000',
            email=fake.email(),
            school=get_sample_school()
        )

        self.assertEquals(str(guardian), guardian.name)

    def test_student_str(self):
        """Test string representation of student object"""
        student = Student.objects.create(
            first_name=fake.name(),
            other_names=fake.name(),
            sex='M',
            status='Boarding',
            date_of_birth=fake.date(),
            place_of_birth=fake.city(),
            residential_address=fake.address(),
            hometown=fake.city(),
            nationality='Ghanaian'
        )

        self.assertEquals(str(student), student.name)
