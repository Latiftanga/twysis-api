
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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
