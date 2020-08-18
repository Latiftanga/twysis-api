import tempfile
import os

from PIL import Image

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.models import Student
from core.models import Class, Grade
from students.serializers import StudentSerializer, StudentDetailSerializer

from students.tests import sample_objects


STUDENTS_URL = reverse('students:student-list')


def image_upload_url(student_id):
    """Return URL for recipe image upload"""
    return reverse('students:student-upload-image', args=[student_id])


def detail_url(student_id):
    """Return details url for student"""
    return reverse('students:student-detail', args=[student_id])


class StudentAPITests(TestCase):
    """Test private available API"""
    def setUp(self):
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
        school = sample_objects.get_school()
        self.staff.school = school
        self.teacher.school = school
        self.client1.force_authenticate(self.staff)
        self.client2.force_authenticate(self.teacher)

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client2.get(STUDENTS_URL)

        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_students(self):
        """Test retrieving students by user school"""
        sample_objects.get_student(sample_objects.get_school())
        sample_objects.get_student(self.staff.school)

        res = self.client1.get(STUDENTS_URL)
        students = Student.objects.filter(school=self.staff.school)
        serializer = StudentSerializer(students, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data, serializer.data)

    def test_retrieve_student_detail(self):
        """Retrieving student detail object"""
        student = sample_objects.get_student(school=self.staff.school)
        guardian = sample_objects.get_guardian(self.staff.school)
        grade = Grade.objects.create(name='SHS 3', year=12)
        grade_class = Class.objects.create(
            division='P',
            grade=grade,
            programme=sample_objects.get_programme(),
            school=self.staff.school
        )
        house = sample_objects.get_house(self.staff.school)
        student.grade_class = grade_class
        student.house = house
        student.guardians.add(guardian)
        student.save()

        url = detail_url(student.id)

        res = self.client1.get(url)
        serializer = StudentDetailSerializer(student)
        self.assertEquals(res.data, serializer.data)

    def test_create_basic_student(self):
        """Test creating student only required fields"""
        payload = sample_objects.get_student_dafault_payload(
            school=self.staff.school
        )
        res = self.client1.post(STUDENTS_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        student = Student.objects.get(id=res.data['id'])

        self.assertEquals(payload['first_name'], student.first_name)

    def test_create_student_with_guardian_class_and_house(self):
        """Test creating a student with guardians"""
        guardian1 = sample_objects.get_guardian(school=self.staff.school)
        guardian2 = sample_objects.get_guardian(school=self.staff.school)
        shs_2 = Grade.objects.create(name='SHS2', year=11)
        programme = sample_objects.get_programme()
        grade_class = Class.objects.create(
            division='J',
            grade=shs_2,
            programme=programme,
            school=self.staff.school
        )
        house = sample_objects.get_house(school=self.staff.school)

        payload = sample_objects.get_student_dafault_payload(
            grade_class=grade_class.id,
            house=house.id,
            guardians=[guardian1.id, guardian2.id]
        )

        res = self.client1.post(STUDENTS_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        student = Student.objects.get(id=res.data['id'])
        guardians = student.guardians.all()
        self.assertEquals(guardians.count(), 2)
        self.assertIn(guardian1, guardians)
        self.assertIn(guardian2, guardians)


class StudentImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.staff = get_user_model().objects.create_staff(
            'user@twysolution.com',
            'testpassword'
        )
        self.client.force_authenticate(self.staff)
        self.staff.school = sample_objects.get_school()
        self.student = sample_objects.create_student(school=self.staff.school)

    def tearDown(self):
        self.student.image.delete()

    def test_upload_image_to_student(self):
        """Test uploading image to student"""
        url = image_upload_url(self.student.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)  # to start reading the file from the begining
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.student.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.student.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.student.id)

        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
