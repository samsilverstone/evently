from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import CreateUserSerializer,ChangePasswordSerializer
from rest_framework import authentication
import jwt,json


class LoginAPI(APIView):
        
    def post(self,request,*args,**kwargs):
        if not request.data:
            return Response({'Error':"Please provide username/password"},status=400)

        username=request.data["username"]
        password=request.data["password"]
        try:
            user=User.objects.get(username=username,password=password)
        except User.DoesNotExist:
            return Response({"Error":"Invalid username/password"},status=400)

        if user:
            _id=str(user.id)
            payload={
                'id':_id,
                'email':user.email
            }
            jwt_token=jwt.encode(payload,'JSONwebtoken',algorithm='HS256')
            print(jwt_token)
            return Response({'token':jwt_token},status=200,content_type="application/json")
        else:
            return Response(
            json.dumps({'Error':'Invalid Credentials'}),
            status=400,
            content_type="application/json"
            )

class RegistrationAPI(APIView):

    def post(self,request,*args,**kwargs):
        serializer=CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
        payload={
            'id':user.id,
            'email':user.email
        }
        print(type(user.id))
        jw_token=jwt.encode(payload,'JSONwebtoken',algorithm='HS256')
        print(jw_token)
        return Response({
            "user":[serializer.data["username"],serializer.data["email"]],
            "token":jw_token
        })

class ResetPasswordAPI(APIView):
    
    def post(self,request,*args,**kwargs):
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        