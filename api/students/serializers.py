from rest_framework.serializers import ModelSerializer
from students import models


class ClassSerializer(ModelSerializer):
    """Class serializer model"""

    class Meta:
        model = models.Class
        fields = ('id', 'name', 'programme', 'programme_division', 'year')
        read_only_fields = ('id', 'name')
