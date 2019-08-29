from rest_framework import serializers
from rest_framework import relations
from .models import User
from django.contrib.auth import authenticate
from .utils import jwt_response_payload_handler
from rest_framework_jwt.settings import api_settings
import uuid

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class CreateUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    token=serializers.SerializerMethodField(read_only=True)
    message=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password',
            'password2',
            'token',
            'message'
        ]
        extra_kwargs={'password':{'write_only':True}}
    
    def validate(self,data):
        pw=data.get('password')
        pw2=data.get('password2')
        if pw!=pw2:
            raise serializers.ValidationError("Passwords do not match!.Please try again.")
        return data

    def validate_password(self,value):
        if len(value)<8:
            raise serializers.ValidationError("Password length is too short.Mininum length should be greater than 8") 
        else:
            return value
    def get_token(self,obj):
        user=obj
        request=self.context.get('request')
        payload=jwt_payload_handler(user)
        partial_token=jwt_encode_handler(payload)
        token=jwt_response_payload_handler(partial_token,user,request=request)
        return token

    def validate_email(self,value):
        qs=User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value
    
    def validate_username(self,value):
        qs=User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value
    
    def get_message(self,obj):
        return "Thank you for registering. Please verify your account before continuing.    "

    def create(self,validated_data):
        _id=str(uuid.uuid1())
        username=validated_data.get('username')
        password=validated_data.get('password')
        email=validated_data.get('email')
        # print(username,email,password)
        user_obj=User.objects.create(id=_id,username=username,email=email)
        user_obj.set_password(password)
        # user_obj.is_active=False
        user_obj.save()
        print(user_obj)
        return user_obj


class ChangePasswordSerializer(serializers.Serializer):
    Old_Password=serializers.CharField(style={'input_type':'password'},write_only=True)
    New_Password=serializers.CharField(style={'input_type':'password'},write_only=True)
    New_Password2=serializers.CharField(style={'input_type':'password'},write_only=True)


    def validate(self,data):
        pass1=data.get('New_Password')
        pass2=data.pop('New_Password2')
        print(pass1)
        print(pass2)
        if pass1!=pass2:
            raise serializers.ValidationError('Passwords do not match!')
        return data
    

class LoginSerializer(serializers.Serializer):

    username=serializers.CharField()
    password=serializers.CharField(style={'input_type':'password'},write_only=True)

    def validate_username(self,value):
        if value=="":
            return serializers.ValidationError("Username cannot be left blank")
        return value
    
    def validate_password(self,value):
        if value=="":
            return serializers.ValidationError("Password Field cannot be left blank")
        return value
    
class ForgotPasswordSerializer(serializers.Serializer):

    username=serializers.CharField()




