from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import generics
from django.contrib.auth import authenticate,get_user_model
from django.db.models import Q
from .serializers import CreateUserSerializer,ChangePasswordSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.settings import api_settings
from .utils import jwt_response_payload_handler
from .permissions import IsOwnerOrReadOnly
import jwt,json

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginAPI(APIView):
    permission_classes=[IsOwnerOrReadOnly]  
    def post(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return Response({'token':'You are already authenticated'},status=400) 
        data=request.data
        username=data.get('username','')
        password=data.get('password','')
        user=authenticate(username=username,password=password)
        qs=User.objects.filter(Q(username__iexact=username)|Q(email__iexact=username)).distinct()
        if qs.count()==1:
            user_obj=qs.first()
            if user_obj.check_password(password):
                user=user_obj
                payload=jwt_payload_handler(user)
                token_partial=jwt_encode_handler(payload)
                token=jwt_response_payload_handler(token_partial,user,request=request)
                return Response(token)


class RegistrationAPI(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=CreateUserSerializer
    permission_class=[]


class ResetPasswordAPI(generics.CreateAPIView):
    
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    serializer_class=ChangePasswordSerializer
    
    def get_serializer_context(self,*args,**kwargs):
        return {'request':self.request}