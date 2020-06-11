from students.models import Class, House, Guardian, Student
from students import serializers
from core.views import CreateRetrieveUpdateViewSet
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsStaff


class ClassViewSets(CreateRetrieveUpdateViewSet):
    """Manage classes in the database """

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Class.objects.all().order_by('year')
    serializer_class = serializers.ClassSerializer


class HouseViewSets(CreateRetrieveUpdateViewSet):
    """Manage houses in the database"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = House.objects.all().order_by('name')
    serializer_class = serializers.HouseSerializer


class GuardianViewSets(CreateRetrieveUpdateViewSet):
    """Manage students Guardians in the database"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Guardian.objects.all()
    serializer_class = serializers.GuardianSerializer


class StudentViewSets(CreateRetrieveUpdateViewSet):
    """Manage students CRUD in the database"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.StudentDetailSerializer
        return self.serializer_class
