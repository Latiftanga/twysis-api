from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from students.models import Class
from students.serializers import ClassSerializer


class ClassViewSets(GenericViewSet, mixins.ListModelMixin):
    """Manage classes in the database """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get_queryset(self):
        """Return classes for authenticated user school"""
        return self.queryset.filter(school=self.request.user.school)
