from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.models import Class
from core.models import School, Programme

from core.tests.faker import fake

CLASS_URL = reverse('students:class-list')


def get_sample_school():
    return School.objects.create(
        name=fake.name(),
        address=fake.address(),
        city=fake.city(),
        region=fake.region()
    )


def get_sample_programme():
    name = fake.name()
    return Programme.objects.create(
        name=name,
        short_name=name[0:4]
    )


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
        school = get_sample_school()
        self.staff.school = school
        self.teacher.school = school
        self.client1.force_authenticate(self.staff)
        self.client2.force_authenticate(self.teacher)

    def test_retrieving_classes_by_user_not_admin(self):
        """Test retrieving classes by other auth users who are not admin users"""
        programme1 = get_sample_programme()

        Class.objects.create(
            programme=programme1,
            programme_division='A',
            year=1,
            school=self.teacher.school
        )
        Class.objects.create(
            programme=programme1,
            programme_division='B',
            year=1,
            school=self.teacher.school
        )

        res = self.client2.get(CLASS_URL)

        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_classes_limited_authenticated_admin_user(self):
        """Test that classes retrieved are limited to authenticated staff user school"""

        programme1 = get_sample_programme()
        programme2 = get_sample_programme()
        clas = Class.objects.create(
            programme=programme1,
            programme_division='C',
            year=1,
            school=self.staff.school
        )
        Class.objects.create(
            programme=programme2,
            programme_division='D',
            year=1,
            school=get_sample_school()
        )

        res = self.client1.get(CLASS_URL)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data[0]['programme_division'], clas.programme_division)

    def test_create_class_success(self):
        """Test creating class successful"""
        p1 = get_sample_programme()
        payload = {
            'programme': p1.id,
            'programme_division': 'H',
            'year': 1,
        }

        res = self.client1.post(CLASS_URL, payload)

        exists = Class.objects.filter(
            programme_division='H',
            school=self.staff.school
        ).exists()

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_class_invalid(self):
        """Test creating an invalid class"""
        payload = {
            'programme': get_sample_programme(),
            'programme_division': '',
            'year': 2,
        }
        res = self.client1.post(CLASS_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
