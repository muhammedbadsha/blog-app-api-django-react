# inside app imports
from .models import User
# restframeworks

from rest_framework.views import APIView,Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ResgisterSerializer,UserView,OTPVerification
from rest_framework.decorators import action
# django 
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
# from django.contrib import sessions
#inbuid methods
from datetime import timezone,datetime,timedelta
import uuid


# Create your views here.

"""send email notification """

def email_sending_otp(email,otp):
    subject = "BLOGGER HUB Email verification "
    message = f"This is your email verification OTP' is {otp}"
    from_email = settings.EMAIL_HOST_USER
    try:
        send_mail(subject,message, from_email, [email])
    except Exception as e:
        print(e)
    print(email,"sent")
    return Response({'li':'success','status':status.HTTP_200_OK},)
        
""" registration of users"""
class RegisterPage(APIView):
    def get(self,request):
        user = User.objects.all()
        serializer = ResgisterSerializer(user, many=True)
        if serializer is not None:
            return Response({'data':serializer.data})
        else:
            return Response({'status':status.HTTP_204_NO_CONTENT})
    @action(detail=False, methods=['POST'])
    def post(self, request):
            data = request.data
            email = data['email']
            otp = str(uuid.uuid4())[:6]
            print('this work')
            try:
                user = get_list_or_404(User,email = email)[0]
            except:
                user = None
            print(user)
            if user is None:
                print('user is none')
                serializer = ResgisterSerializer(data=data, many=False)
                if serializer.is_valid():
                    print('valid')
                    user = serializer.create(validated_data=data)
                    user.email_otp = otp
                    user.email_otp_expiry = datetime.now() + timedelta(minutes=10)
                    user.max_otp_try = int(user.max_otp_try) - 1
                    user_session = request.session
                    if user_session is not None:
                        request.session.flush()
                        request.session['email'] = user.id
                    else:
                        request.session['email'] = user.id
                    serializer.update(user)            
#email  
                    email = email_sending_otp(email,otp)

                    return Response({'data':serializer.data})
                return Response({'data':serializer.errors})
                
            elif user is not None and user.email_verify==False and user.email:
                serializer = ResgisterSerializer(instance=user, data = data)
                
                if serializer.is_valid():
                    if user.email_otp_out is None and int(user.max_otp_try) >= 0:
                        user.user_name = serializer.validated_data['email'].split('@')[0]
                        user.email_otp = otp
                        user.email_otp_expiry = datetime.now() + timedelta(minutes=10)
                        user.max_otp_try = int(user.max_otp_try) - 1
                        # user.save()
                        session = request.session
                        if session is not None:
                            session.flush() 
                            request.session['email'] = user.id
                        else:
                            user.session['email'] = user.id

                        serializer.update(user)
#email  
                        email = email_sending_otp(email,otp)
                        return Response({'data':serializer.data})
                    elif int(user.max_otp_try) >= 0 and user.email_otp_out <= datetime.now():
                        user.max_otp_try = int(settings.MAX_OTP_TRY) - 1
                        user.email_otp_out = None
                        user.save()
                        session = request.session
                        if session is not None:
                            session.flush() 
                            request.session['email'] = user.id
                        else:
                            user.session['email'] = user.id

                        serializer.update(user)
#email  
                        email = email_sending_otp(email,otp)

                    else:
                        user.email_otp_out = datetime.now() + timedelta(hours=1)
                        user.save()
                        return Response({'data': 'please waite 1 houre your otp try is out'})
                return Response({'data':serializer.errors})
            else:
                return Response({'data':'faild','status':'user is already registered and verifyed go to login page'})


              




class HomePage(APIView):
    def get(self,request):
        pass

    def post(self,request):
        pass

