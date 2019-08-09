from rest_framework import serializers
from rest_framework import relations
from .models import User
import uuid

class CreateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=('id','password','username','email')
        extra_kwargs={'password':{'write_only':True}}
    
    def validate_password(self,value):
        if len(value)<8:
            raise serializers.ValidationError("Password length is too short.Mininum length should be greater than 8") 
        else:
            return value
    
    def create(self,validated_data):
        _id=str(uuid.uuid1())
        password=validated_data["password"]
        username=validated_data["username"]
        email=validated_data["email"]
        print(password)
        return User.objects.create(id=_id,password=password,username=username,email=email)


class ChangePasswordSerializer(serializers.Serializer):
    oldpassword=serializers.CharField()
    newpassword=serializers.CharField()

    def validate_oldpassword(value):
        

    def create(self,validated_data):
        pass

