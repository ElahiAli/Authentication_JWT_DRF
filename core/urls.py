from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('users',views.UserView,basename='user')


urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('',include(router.urls)),
]





