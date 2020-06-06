from students.models import Class, House
from students.serializers import ClassSerializer, HouseSerializer
from core.views import CreateRetrieveUpdateViewSet
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsStaff


class ClassViewSets(CreateRetrieveUpdateViewSet):
    """Manage classes in the database """

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Class.objects.all().order_by('year')
    serializer_class = ClassSerializer


class HouseViewSets(CreateRetrieveUpdateViewSet):
    """Manage houses in the database"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = House.objects.all().order_by('name')
    serializer_class = HouseSerializer
