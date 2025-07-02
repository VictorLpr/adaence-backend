from rest_framework import serializers
from .models import Cities, Activities, Elders, Volunteers, Appointments


class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ['id', 'title', 'zipcode', 'lat', 'lng']


class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ['id', 'name']

