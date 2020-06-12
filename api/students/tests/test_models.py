from unittest.mock import patch
from django.test import TestCase
from students import models
from students.tests import sample_objects
from core.tests.faker import fake


class ModelTest(TestCase):
    """Students models tests"""

    def test_class_str(self):
        """Test the string representation of class object"""
        programme = sample_objects.get_programme()

        clas = models.Class.objects.create(
            programme=programme,
            programme_division='A',
            year=1,
        )

        self.assertEquals(str(clas), clas.name)

    def test_house_str(self):
        """Test the string representation of house"""
        school = sample_objects.get_school()
        house = models.House.objects.create(name='Masroor', school=school)

        self.assertEqual(str(house), house.name)

    def test_guardian_str(self):
        """Test the string representation of student guardian"""
        guardian = models.Guardian.objects.create(
            name=fake.name(),
            address=fake.address(),
            relation=fake.guardian_relation(),
            phone='0200000000',
            email=fake.email,
            school=sample_objects.get_school()
        )

        self.assertEquals(str(guardian), guardian.name)

    def test_student_str(self):
        """Test string representation of student object"""
        student = sample_objects.get_student(sample_objects.get_school())

        self.assertEquals(str(student), student.name)

    @patch('uuid.uuid4')
    def test_student_filename_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test uuid'
        mock_uuid.return_value = uuid

        file_path = models.student_image_file_path(None, 'myimage.jpg')

        exp_file_path = f'uploads/students/{uuid}.jpg'

        self.assertEqual(file_path, exp_file_path)
