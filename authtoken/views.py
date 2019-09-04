from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import generics,status
from django.contrib.auth import authenticate,get_user_model
from django.db.models import Q
from .serializers import CreateUserSerializer,ChangePasswordSerializer,LoginSerializer,ForgotPasswordSerializer
from location.Function.formatdata import formatdata
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework_jwt.settings import api_settings
from .utils import jwt_response_payload_handler
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests
import base64
import shutil
import jwt,json

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginAPI(APIView):

    permission_classes=[IsOwnerOrReadOnly]  

    def post(self,request,*args,**kwargs):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.is_authenticated:
                return Response({'token':'You are already authenticated'},status=400) 
            data=request.data
            username=data.get('username','')
            password=data.get('password','')
            qs=User.objects.filter(Q(username__iexact=username)|Q(email__iexact=username)).distinct()
            if qs.count()==1:
                user_obj=qs.first()
                if user_obj.check_password(password):
                    user=user_obj
                    payload=jwt_payload_handler(user)
                    token_partial=jwt_encode_handler(payload)
                    token=jwt_response_payload_handler(token_partial,user,request=request)
                    return Response(token)
                return Response({'password':'Incorrect Password'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'user':'User does not exist'},status=status.HTTP_404_NOT_FOUND)


class RegistrationAPI(generics.CreateAPIView):

    queryset=User.objects.all()
    permission_class=[]


class ResetPasswordAPI(APIView):
        
    def post(self,request):
        print(request.user)
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data.get('Old_Password'))
            if not request.user.check_password(serializer.validated_data.get('Old_Password')):
                return Response({'old_password':'Wrong password'},
                status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.validated_data.get('New_Password'))
            request.user.save()
            return Response({'status':'Password Changed'},status=status.HTTP_200_OK)

        return Response(serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self,*args,**kwargs):
        return {'request':self.request}
    
class ForgotPasswordAPI(APIView):

    def post(self,request,*args,**kwargs):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username=serializer.validated_data.get("username")
            qs=User.objects.filter(Q(username__iexact=username)|Q(email__iexact=username))
            if qs.count()==1:
                user=qs.first()
                key='AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ'
                # url='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=restaurant&key=AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ'
                # url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU&key=AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ'
                url='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Saket%20New%20Delhi&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ'
                # url='https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJjRuIiTiuEmsRCHhYnrWiSok&fields=website,reviews,formatted_address,formatted_phone_number&key=AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ'
                nextpage='https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=CpQCAgEAAFxg8o-eU7_uKn7Yqjana-HQIx1hr5BrT4zBaEko29ANsXtp9mrqN0yrKWhf-y2PUpHRLQb1GT-mtxNcXou8TwkXhi1Jbk-ReY7oulyuvKSQrw1lgJElggGlo0d6indiH1U-tDwquw4tU_UXoQ_sj8OBo8XBUuWjuuFShqmLMP-0W59Vr6CaXdLrF8M3wFR4dUUhSf5UC4QCLaOMVP92lyh0OdtF_m_9Dt7lz-Wniod9zDrHeDsz_by570K3jL1VuDKTl_U1cJ0mzz_zDHGfOUf7VU1kVIs1WnM9SGvnm8YZURLTtMLMWx8-doGUE56Af_VfKjGDYW361OOIj9GmkyCFtaoCmTMIr5kgyeUSnB-IEhDlzujVrV6O9Mt7N4DagR6RGhT3g1viYLS4kO5YindU6dm3GIof1Q&key=YOUR_API_KEY'
                response=requests.get(url)
                # print(response.content.replace)
                print(response.headers['Content-Type'])
                # res=response.body
                # return Response({"status":response.content})
                return Response({"status":response.json()})    
    
    def send_Mail(self):
        message = Mail(
        from_email='sanjaysajwan765@gmail.com',
        to_emails='ssajwan.deligence@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
                
class placeDetailsAPI(APIView):

    def get(self,request,*args,**kwargs):
        location=request.query_params.get('location')
        category=request.query_params.get('category')
        radius=request.query_params.get('radius',2000)
        feature=request.query_params.get('rankby','')
        print(feature)
        key='AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ'
        response=requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=geometry&key={}".format(location,key))
        res=response.json()
        lat=res["candidates"][0]["geometry"]["location"]["lat"]
        lng=res["candidates"][0]["geometry"]["location"]["lng"]
        data={}
        if feature=='distance':
            response=requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&rankby=distance&type={}&keyword={}&key={}".format(lat,lng,category,category,key))
            data=response.json()
        else:
            response=requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&keyword={}&key={}".format(lat,lng,radius,category,category,key))
            data=response.json()
            
       
        # photo_reference=data["results"][3]["photos"][0]["photo_reference"]
        # response=requests.get("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}".format(photo_reference,key))
        # r = requests.get("https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={}&key={}".format(photo_reference,key), stream=True)
        # print(r)
        # if r.status_code == 200:
        #     data=bytes()
        #     for chunk in r:
        #         data+=chunk
        # # print(response.headers['Content-Type'])
        # img_string_data=data.hex()
        # img_byte_data=str.encode(img_string_data)
        # print(img_byte_data)
        # img_decode=base64.decodebytes(img_byte_data)
        # with open('img_data.jpeg','wb') as img:
        #     img.write(img_decode)
        nearbyarr=[]
        for i in range(len(data["results"])):
            nearbyarr.append(formatdata(data["results"][i]))
        return Response({
            "data":nearbyarr,   
            "nextpagetoken":data["next_page_token"] if data["next_page_token"] else None,
            "origin":{
                "lat":lat,
                "lng":lng
            }   
        })
    

class nextPageDetailsAPI(APIView):

    def get(self,request,*args,**kwargs):
        next_page_token=request.query_params.get('next_page_token')
        key="AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ"
        response=requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}".format(next_page_token,key))
        data=response.json()
        nearbyarr=[]
        for i in range(len(data["results"])):
            nearbyarr.append(formatdata(data["results"][i]))
        return Response({
            "data":nearbyarr,
            "nextpagetoken":data["next_page_token"] if "next_page_token" in data.keys() else None
            })

class IndividualplaceDetailsAPI(APIView):
    
    def get(self,request,*args,**kwargs):
        place_id=request.query_params.get("place_id")
        response=requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid={}&fields=name,place_id,formatted_address,rating,opening_hours,website,review,formatted_phone_number&key=AIzaSyA4mI-Wb-OWrtHlste2j8GbuFdD4CvzYbQ".format(place_id))
        data=response.json()["result"]
        open=[]
        if "opening_hours" in data.keys():
            if "weekday_text" in data["opening_hours"].keys():
                open=data["opening_hours"]["weekday_text"]
            else:
                open=None
        else:
            open=None
        if response.json()["status"]=="OK":
            formatted_data={
                "formatted_address":data["formatted_address"] if "formatted_address" in data.keys() else None,
                "formatted_phone_number":data["formatted_phone_number"] if "formatted_phone_number" in data.keys() else None,
                "opening_hours":open,
                "website":data["website"] if "website" in data.keys() else None,
                "place_id":data["place_id"] if "place_id" in data.keys() else None
            }
            return Response({
             "data":formatted_data
             })
        else:
            return Response({
                "data":"Some Error Occured"
            },status=status.HTTP_400_BAD_REQUEST)