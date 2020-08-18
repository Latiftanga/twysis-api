from rest_framework import serializers
from core.models import House, Class, Grade, Programme


class ProgrammeSerializer(serializers.ModelSerializer):
    """Programmes levels serializer"""

    class Meta:
        model = Programme
        fields = ('id', 'name', 'code')
        read_only_fields = ('id', )


class GradeSerializer(serializers.ModelSerializer):
    """Grade levels serializer"""

    class Meta:
        model = Grade
        fields = ('id', 'name', 'year')
        read_only_fields = ('id', )


class HouseSerializer(serializers.ModelSerializer):
    """House serializer model"""

    class Meta:
        model = House
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ClassSerializer(serializers.ModelSerializer):
    """Student class serializer"""

    class Meta:
        model = Class
        fields = ('id', 'name', 'grade', 'programme')
        read_only_fields = ('id', )
