from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.conf import settings
import uuid


User = get_user_model()



class ResgisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    
    class Meta:
        model = User
        fields = ['id', 'profile_pic','first_name','last_name', 'email','password','confirm_password']


    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        return data
    
   
    def create(self, validated_data):
        
        email_otp = str(uuid.uuid4())[:6]
        email_expiry = datetime.now() + timedelta(minutes = 5)

        user = User(
            profile_pic = validated_data['profile_pic'],
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name'],
            
            email = validated_data['email'],
            
            max_otp_try = settings.MAX_OTP_TRY,
            email_otp = email_otp,
            email_otp_expiry = email_expiry,
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance,**validated_data):
        email_otp = str(uuid.uuid4())[:6]
        email_expiry = datetime.now() + timedelta(minutes = 5)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        print(email_otp)
        instance.about = validated_data.get('about', instance.about)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.email = validated_data.get('email', instance.email)
        print(instance.email_otp,'iiiiiiiiiiii')
        instance.email_otp = email_otp
        print(instance.email_otp)
        instance.email_otp_expiry = email_expiry

        instance.save()