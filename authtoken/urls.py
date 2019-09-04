from django.urls import path
from .views import RegistrationAPI,LoginAPI,ResetPasswordAPI,ForgotPasswordAPI,placeDetailsAPI,nextPageDetailsAPI,IndividualplaceDetailsAPI

urlpatterns = [
    path('signup/',RegistrationAPI.as_view()),
    path('login/',LoginAPI.as_view()),
    path('resetpassword/',ResetPasswordAPI.as_view()),
    path('forgotpass/',ForgotPasswordAPI.as_view()),
    path('placedetail/',placeDetailsAPI.as_view()),
    path('nextpagedetail/',nextPageDetailsAPI.as_view()),
    path('individualplace',IndividualplaceDetailsAPI.as_view())
]