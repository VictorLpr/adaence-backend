from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import CitiesViewSet, ActivitiesViewSet, ElderViewSet, LoginView

router = DefaultRouter()
router.register(r'cities', CitiesViewSet, basename='cities')
router.register(r'activities', ActivitiesViewSet, basename='activities')
router.register(r'elders', ElderViewSet, basename='elders')

urlpatterns = [
    # API endpoints
    path('api/v1/', include(router.urls)),
    path('login/', LoginView.as_view()),
    # Authentification
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]