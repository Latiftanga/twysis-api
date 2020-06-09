from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.models import Student
from students.serializers import StudentSerializer, StudentDetailSerializer

from students.tests import sample_objects


STUDENTS_URL = reverse('students:student-list')


def detail_url(student_id):
    """Return details url for student"""
    return reverse('students:student-detail', args=[student_id])


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
        school1 = sample_objects.get_school()
        school2 = sample_objects.get_school()
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
        sample_objects.get_student(school=self.staff.school)
        sample_objects.get_student(school=self.teacher.school)

        res = self.client1.get(STUDENTS_URL)
        students = Student.objects.filter(school=self.staff.school)
        serializer = StudentSerializer(students, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data, serializer.data)

    def test_retrieve_student_detail(self):
        """Retrieving student detail object"""
        student = sample_objects.get_student(school=self.staff.school)
        student.guardians.add(sample_objects.get_guardian(school=self.staff.school))

        STUDENT_DETAIL_URL = detail_url(student.id)

        res = self.client1.get(STUDENT_DETAIL_URL)

        serializer = StudentDetailSerializer(student)

        self.assertEquals(res.data, serializer.data)
