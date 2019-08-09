from django.urls import path
from .views import RegistrationAPI,LoginAPI

urlpatterns = [
    path('signup/',RegistrationAPI.as_view()),
    path('login/',LoginAPI.as_view())
]