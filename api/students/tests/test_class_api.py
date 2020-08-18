from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.tests import sample_objects
from core.models import Grade, Class

CLASS_URL = reverse('class-list')


class PublicClassAPITest(TestCase):
    """Test publicly available class API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving classes"""
        res = self.client.get(CLASS_URL)

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClassAPITests(TestCase):
    """Test the private availabe class API"""

    def setUp(self):
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.staff = get_user_model().objects.create_staff(
            email='staff@twysolutions.com',
            password='staff@pass',
        )
        self.teacher = get_user_model().objects.create_teacher(
            email='teacher@twysolutions.com',
            password='teacher@pass',
        )
        school = sample_objects.get_school()
        self.staff.school = school
        self.teacher.school = school
        self.client1.force_authenticate(self.staff)
        self.client2.force_authenticate(self.teacher)

    def test_retrieving_classes_by_user_not_admin(self):
        """Test retrieving classes by other auth users"""
        programme1 = sample_objects.get_programme()
        grade_shs_1 = Grade.objects.create(
            name='SHS 1',
            year=10
        )
        grade_shs_2 = Grade.objects.create(
            name='SHS 2',
            year=11
        )

        Class.objects.create(
            division='A',
            grade=grade_shs_1,
            programme=programme1,
            school=self.teacher.school
        )
        Class.objects.create(
            division='B',
            grade=grade_shs_2,
            programme=programme1,
            school=self.teacher.school
        )

        res = self.client2.get(CLASS_URL)

        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_classes_limited_authenticated_admin_user(self):
        """Test that classes retrieved are limited to authenticated staff"""

        programme1 = sample_objects.get_programme()
        programme2 = sample_objects.get_programme()
        shs_3 = Grade.objects.create(
            name='SHS 3',
            year=12,
        )
        shs_2 = Grade.objects.create(
            name='SHS 2',
            year=11,
        )
        clas = Class.objects.create(
            division='C',
            grade=shs_2,
            programme=programme2,
            school=self.staff.school
        )
        Class.objects.create(
            division='D',
            grade=shs_3,
            programme=programme1,
            school=sample_objects.get_school()
        )

        res = self.client1.get(CLASS_URL)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(
            res.data[0]['name'],
            clas.name
        )

    def test_create_class_success(self):
        """Test creating class successful"""
        p1 = sample_objects.get_programme()
        grade = Grade.objects.create(
            name='SHS 1',
            year=10,
        )
        payload = {
            'division': 'H',
            'programme': p1.id,
            'grade': grade.year,
            'school': self.staff.school.id,
        }

        res = self.client1.post(CLASS_URL, payload)

        # exists = Class.objects.filter(
        #     division='H',
        #     school=self.staff.school
        # ).exists()

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        # self.assertTrue(exists)

    def test_create_class_invalid(self):
        """Test creating an invalid class"""
        p1 = sample_objects.get_programme()
        # grade = Grade.objects.create(
        #     name='SHS 1',
        #     year=10,
        # )
        payload = {
            'programme': p1.id
        }
        res = self.client1.post(CLASS_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
