from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import House
from students.tests.sample_objects import get_school
from core.tests.faker import fake

HOUSE_URL = reverse('house-list')


class PublicHouseAPITest(TestCase):
    """Test publicly available house api"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving Houses"""
        res = self.client.get(HOUSE_URL)

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHouseAPITests(TestCase):
    """Test the private available api for houses"""
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
        self.staff.school = get_school()
        self.teacher.school = get_school()
        self.client1.force_authenticate(self.staff)
        self.client2.force_authenticate(self.teacher)

    def test_retrieving_house_by_teacher_user(self):
        """Test retrieving houses for teacher user not an admin """

        House.objects.create(name=fake.name(), school=self.teacher.school)
        House.objects.create(name=fake.name(), school=self.teacher.school)

        res = self.client2.get(HOUSE_URL)

        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_houses_school_admin(self):
        """Test retrieving houses for the authenticated user(admin) school"""
        school2 = get_school()
        house1 = House.objects.create(
            name=fake.name(),
            school=self.staff.school
        )
        House.objects.create(name=fake.name(), school=school2)

        res = self.client1.get(HOUSE_URL)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data[0]['name'], house1.name)

    def test_create_house_success(self):
        """Creating a new by admin successful"""
        payload = {'name': 'Masroor'}

        res = self.client1.post(HOUSE_URL, payload)

        exists = House.objects.filter(name=payload['name']).exists()

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_house_invalid(self):
        """"Creating an invalid house by admin"""
        payload = {'name': ''}

        res = self.client1.post(HOUSE_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
