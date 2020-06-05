import uuid

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from students.models import Class
from students.serializers import ClassSerializer
from core.models import School, Programme


CLASS_URL = reverse('students:class-list')


def get_sample_school():
    name = str(uuid.uuid4())
    return School.objects.create(
        name=name[:5],
        address='some location',
        city='Wa',
        region='UW'
    )


def get_sample_programme():
    name = str(uuid.uuid4())
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
        self.client = APIClient()
        self.user = get_user_model().objects.create_staff(
            email='staff@twysolutions.com',
            password='staff@pass',
        )
        school = get_sample_school()
        self.user.school = school
        self.client.force_authenticate(self.user)

    def test_retrieve_classes(self):
        """Test retrieving tags limited school"""
        programme1 = get_sample_programme()
        Class.objects.create(
            programme=programme1,
            programme_division='A',
            year=1,
            school=self.user.school
        )
        Class.objects.create(
            programme=programme1,
            programme_division='B',
            year=1,
            school=self.user.school
        )

        res = self.client.get(CLASS_URL)

        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)

    def test_classes_limited_authenticated_user_school(self):
        """Test that classes retrieved are limited to authenticated user school"""
        user2 = get_user_model().objects.create_staff(
            email='staff2@twysolutions.com',
            password='staff2@pass',
        )
        school2 = get_sample_school()
        user2.school = school2
        programme1 = get_sample_programme()
        programme2 = get_sample_programme()
        clas = Class.objects.create(
            programme=programme1,
            programme_division='C',
            year=1,
            school=self.user.school
        )
        Class.objects.create(
            programme=programme2,
            programme_division='D',
            year=1,
            school=user2.school
        )

        res = self.client.get(CLASS_URL)

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

        res = self.client.post(CLASS_URL, payload)

        exists = Class.objects.filter(
            programme_division='H',
            school=self.user.school
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
        res = self.client.post(CLASS_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
