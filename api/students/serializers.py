from rest_framework import serializers
from students import models


class ClassSerializer(serializers.ModelSerializer):
    """Class serializer model"""

    class Meta:
        model = models.Class
        fields = ('id', 'name', 'programme', 'programme_division', 'year')
        read_only_fields = ('id', 'name')


class HouseSerializer(serializers.ModelSerializer):
    """House serializer model"""

    class Meta:
        model = models.House
        fields = ('id', 'name')
        read_only_fields = ('id',)


class GuardianSerializer(serializers.ModelSerializer):
    """Student Guardian Serializer """

    class Meta:
        model = models.Guardian
        fields = ('id', 'name', 'address', 'phone', 'email')
        read_only_fields = ('id',)


class StudentSerializer(serializers.ModelSerializer):
    """Manage students form the database"""
    guardians = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Guardian.objects.all(),
        required=False
    )

    class Meta:
        model = models.Student
        fields = (
            'id',
            'first_name',
            'other_names',
            'sex',
            'status',
            'date_of_birth',
            'place_of_birth',
            'residential_address',
            'hometown',
            'nationality',
            'phone',
            'email',
            'house',
            'clas',
            'guardians',
        )
        read_only_fields = ('id',)


class StudentDetailSerializer(StudentSerializer):
    """Student detail serializer"""
    clas = ClassSerializer(read_only=True)
    house = HouseSerializer(read_only=True)
    guardians = GuardianSerializer(many=True, read_only=True)
