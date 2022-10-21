from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserView, basename='user')
router.register('login', views.LoginView, basename='login')
router.register('resend-email', views.ResendChangeEmailView,
                basename='resend-email')

urlpatterns = [
    path('register/', views.RegisterViewSet.as_view(), name='register'),
    path('verify-email/', views.VerifyEmail.as_view(), name='email-verify'),
    path('', include(router.urls)),

]
