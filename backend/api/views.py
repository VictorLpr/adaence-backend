from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from .models import Cities, Activities, Elders, Volunteers, Appointments
from .serializers import (
    CitiesSerializer, ActivitiesSerializer, ElderSerializer, VolunteerSerializer, AppointmentSerializer
)



class CitiesViewSet(viewsets.ReadOnlyModelViewSet):
    """API pour les villes - lecture seule"""
    queryset = Cities.objects.all().order_by('title')
    serializer_class = CitiesSerializer
    permission_classes = [AllowAny]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['id','title', 'zipcode']


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']  

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteers.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_files = ['city']

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        user = self.request.user

        if user.role == 'volunteer':
            return Appointments.objects.filter(volunteer__user=user)
        elif user.role == 'elder':
            return Appointments.objects.filter(volunteer__user=user)
        
        return Appointments.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
    




class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise ValidationError('Email et mot de passe requis')

        user = authenticate(request, username=email, password=password)

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
     

        token, created = Token.objects.get_or_create(user=user)
        response = Response({
            'message': 'Connexion réussie',
            'user': {
                'id': user.id, 
                'email': user.email,
            }
        })
        response.set_cookie(
                'auth_token',
                token.key,
                max_age=3600,
                httponly=True,
                secure=True,  # HTTPS uniquement
                samesite='Strict'
            )
        return response