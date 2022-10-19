from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', views.UserView, basename='user')


urlpatterns = [
    path('register/', views.RegisterViewSet.as_view(), name='register'),
    path('login/', views.Login, name='login'),
    path('verify-email/', views.VerifyEmail.as_view(), name='email-verify'),
    path('', include(router.urls)),

]
