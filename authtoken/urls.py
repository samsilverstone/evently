from django.urls import path
from .views import RegistrationAPI,LoginAPI,ResetPasswordAPI

urlpatterns = [
    path('signup/',RegistrationAPI.as_view()),
    path('login/',LoginAPI.as_view()),
    path('resetpassword/',ResetPasswordAPI.as_view())
]