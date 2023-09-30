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

"""OTP Verification """

class VerifyEmailOTP(APIView):
    query_set = User.objects.all()
    serializer = ResgisterSerializer
    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404
    # print(request.COOKIES['email'])
    @action(detail=True, methods=['POST'])
    def post(self, request,id):
        print('inside')
        instance = self.get_object(id)
        print(instance.email_otp,instance.email_verify)
        
        serializer = OTPVerification(instance=instance,data=request.data)
        if serializer.is_valid():
            otp = request.data['otp']
            print('serializer data,',otp )
            print(str(instance.email_otp_expiry)[:19])
            print(str(datetime.now())[:19])
        # print(request)
            if not instance.email_verify and instance.email_otp == otp and instance.email_otp_expiry and str(datetime.now())[:19] < str(instance.email_otp_expiry)[:19]:
                instance.email_verify = True
                instance.email_otp_expiry = None
                instance.max_otp_try = settings.MAX_OTP_TRY
                instance.email_otp_out = None
                instance.save()

                return Response("success otp is verified",status=status.HTTP_200_OK)
        print('bad error',instance)
        return Response('verification is failed',status=status.HTTP_400_BAD_REQUEST)
    @action(detail = True, methods=['put'])
    def regenerate_otp(self, request,id=None):
        instance = self.get_object(id)
        if (instance.max_otp_try) == 0 and str(datetime.now())[:19] < str(instance.email_otp_out)[:19]:
            return Response('maximum otp tries exceeded, try after 1 hour',status=status.HTTP_400_BAD_REQUEST)
        otp = str(uuid.uuid4())[:6]
        otp_expires = datetime.now() + timedelta(minutes=10)
        max_otp_tries = int(instance.max_otp_try)-1

        instance.email_otp = otp
        instance.email_otp_expiry = otp_expires
        instance.max_otp_try = max_otp_tries
        if max_otp_tries == 0 and str(datetime.now())[:19] >= str(instance.email_otp_out)[:19]:
            instance.email_otp_out =datetime.now() + timedelta(hours=1)
            instance.max_otp_try -= 1 
        elif max_otp_tries == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        #email sending
            email_sending_otp(instance.email,otp)
        else:
            instance.email_otp_out = None
            instance.max_otp_try = max_otp_tries
        #email sending
            email_sending_otp(instance.email,otp)

        instance.save()
        return Response('successfully otp send',status=status.HTTP_200_OK)
              




class HomePage(APIView):
    def get(self,request):
        pass

    def post(self,request):
        pass

