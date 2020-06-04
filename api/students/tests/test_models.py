from django.test import TestCase

from students.models import Class
from core.models import Programme


class ModelTest(TestCase):
    """Students models tests"""

    def test_class_str(self):
        """Test the string representation of class object"""
        programme = Programme.objects.create(
            name='Agriculture',
            short_name='Agric'
        )

        clas = Class.objects.create(
            programme=programme,
            programme_division='A',
            year=1,
        )

        self.assertEquals(str(clas), clas.name)
