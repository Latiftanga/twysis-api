from rest_framework import serializers
from students import models
from core.serializers import HouseSerializer, ClassSerializer


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
            'admission_id',
            'first_name',
            'last_name',
            'sex',
            'date_of_birth',
            'place_of_birth',
            'residential_address',
            'hometown',
            'nationality',
            'phone',
            'email',
            'status',
            'grade_class',
            'house',
            'guardians',
        )
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
        )


class StudentDetailSerializer(StudentSerializer):
    """Student detail serializer"""
    grade_class = ClassSerializer(read_only=True)
    house = HouseSerializer(read_only=True)
    guardians = GuardianSerializer(many=True, read_only=True)


class StudentImageSerializer(serializers.ModelSerializer):
    """Student image serializer"""

    class Meta:
        model = models.Student
        fields = ('id', 'image')
        read_only_fields = ('id',)
