from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.models import Student
from students.serializers import StudentSerializer
from core.tests.faker import fake
from students.tests.test_class_api import get_sample_school


STUDENTS_URL = reverse('students:student-list')


def get_sample_student(school, **params):
    """create sample student """
    name = fake.name()
    defaults = {
        'first_name': name.split(' ')[0],
        'other_names': name.split(' ')[1],
        'sex': fake.sex(),
        'date_of_birth': fake.date(),
        'place_of_birth': fake.city(),
        'residential_address': fake.address(),
        'hometown': fake.city(),
        'nationality': 'Ghanaian',
        'phone': '0209226608',
        'email': fake.email()
    }
    defaults.update(params)

    return Student.objects.create(school=school, **defaults)


class StudentAPITest(TestCase):
    """Test private available API"""
    def setUp(self):
        self.client = APIClient()
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.staff = get_user_model().objects.create_staff(
            email='staff@twysolutions.com',
            password='staff@password'
        )
        self.teacher = get_user_model().objects.create_teacher(
            email='teacher@twysolutions.com',
            password='teacher@password'
        )
        school1 = get_sample_school()
        school2 = get_sample_school()
        self.staff.school = school1
        self.teacher.school = school2
        self.client1.force_authenticate(self.staff)
        self.client2.force_authenticate(self.teacher)

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(STUDENTS_URL)

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_students(self):
        """Test retrieving students by user school"""
        get_sample_student(school=self.staff.school)
        get_sample_student(school=self.teacher.school)

        res = self.client1.get(STUDENTS_URL)
        students = Student.objects.filter(school=self.staff.school)
        serializer = StudentSerializer(students, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data, serializer.data)
