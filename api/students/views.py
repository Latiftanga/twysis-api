from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from students.models import Guardian, Student
from students import serializers
from core.views import ListCreateReadUpdateViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsStaff


class GuardianViewSets(ListCreateReadUpdateViewSet):
    """Manage students Guardians in the database"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Guardian.objects.all()
    serializer_class = serializers.GuardianSerializer


class StudentGuardiansViewSets(ModelViewSet):
    """Manage students Guardians in the database"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Guardian.objects.all()
    serializer_class = serializers.GuardianSerializer

    def get_queryset(self):
        return Guardian.objects.filter(students__id=self.kwargs['_pk'])

    def perform_create(self, serializer):
        student = Student.objects.get(pk=self.kwargs['_pk'])
        if student:
            guardian = serializer.save(
                school=self.request.user.school,
                created_by=self.request.user.email
            )
            student.guardians.add(guardian)
            student.save()

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user.email
        )


class StudentViewSets(ListCreateReadUpdateViewSet):
    """Manage students CRUD in the database"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.StudentDetailSerializer
        elif self.action == 'upload_image':
            return serializers.StudentImageSerializer
        return self.serializer_class

    @action(methods=['post'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image to student instance"""
        student = self.get_object()
        serializer = self.get_serializer(
            student,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
