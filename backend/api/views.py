from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Cities, Activities, Elders
from .serializers import (
    CitiesSerializer, ActivitiesSerializer, ElderSerializer
)


class CitiesViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les villes - lecture seule"""
    queryset = Cities.objects.all().order_by('title')
    serializer_class = CitiesSerializer
    permission_classes = [AllowAny]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'zipcode']


class ActivitiesViewSet(viewsets.ModelViewSet):
    """API pour les activités"""
    queryset = Activities.objects.all().order_by('name')
    serializer_class = ActivitiesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ElderViewSet(viewsets.ModelViewSet):
    queryset = Elders.objects.all()
    serializer_class = ElderSerializer
    permission_classes = [AllowAny]  


