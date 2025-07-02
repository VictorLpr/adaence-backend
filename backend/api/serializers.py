from rest_framework import serializers
from .models import Cities, Activities, Elders, Volunteers, Appointments, CustomUser, CustomUserManager


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ['id', 'title', 'zipcode', 'lat', 'lng']


class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ['id', 'name']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','first_name','last_name','role','is_active','is_staff']

class ElderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    city = CitiesSerializer
    age = serializers.ReadOnlyField()

    class Meta:
        model = Elders
        fields = ['id', 'user', 'job', 'date_of_birth', 'city', 'description', 'phone_number', 'age']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        elder = Elders.objects.create(user = user, **validated_data)
        return elder
