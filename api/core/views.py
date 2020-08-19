
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import House, Class, Programme, Room, Period
from core.permissions import IsStaff
from core import serializers


class ListCreateReadUpdateViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        return queryset.filter(school=self.request.user.school)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(
            school=self.request.user.school,
            created_by=self.request.user.email
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user.email
        )


class ProgrammeViewSets(viewsets.ModelViewSet):
    """Manage grades in the database"""
    permission_classes = (IsStaff,)
    queryset = Programme.objects.all()
    serializer_class = serializers.ProgrammeSerializer


class ClassViewSets(ListCreateReadUpdateViewSet):
    """Manage classes in the database """
    permission_classes = (IsStaff,)
    queryset = Class.objects.all()
    serializer_class = serializers.ClassSerializer


class RoomViewSets(ListCreateReadUpdateViewSet):
    """Manage class rooms in the database"""
    permission_classes = (IsStaff,)
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer


class PeriodViewSets(ListCreateReadUpdateViewSet):
    """Manage periods in the database"""
    permission_classes = (IsStaff,)
    queryset = Period.objects.all()
    serializer_class = serializers.PeriodSerializer


class HouseViewSets(ListCreateReadUpdateViewSet):
    """Manage houses in the database"""
    permission_classes = (IsStaff,)
    queryset = House.objects.all().order_by('name')
    serializer_class = serializers.HouseSerializer
