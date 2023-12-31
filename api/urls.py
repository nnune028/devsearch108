from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Generate a simple token
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Give us a token to generate a new token. Token with a longer lifespan
    path('projects/<str:pk>/vote/', views.projectVote),
    path('remove-tag/', views.removeTag),
]