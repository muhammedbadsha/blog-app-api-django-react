from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self,  email, password=None,  **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,  **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(auto_created=True,primary_key=True)
    profile_pic = models.ImageField(upload_to='profile/',blank=True,null=True)
    first_name = models.CharField(max_length=250, null=True,)
    last_name = models.CharField(max_length=250)
    bio = models.CharField(max_length=200)
    about = models.CharField(max_length=10000)
    user_name = models.CharField(max_length=250,null=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    email_otp = models.CharField(max_length=6,null=True)
    # cripto_token = models.CharField(max_length=34,null=True)

    # phone_number = PhoneNumberField(blank=True, unique=True,null=True)
    # phone_number_otp = models.CharField(max_length=6,null=True)
    password = models.CharField(max_length=350, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)
    email_otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2,default=settings.MAX_OTP_TRY)
    email_otp_out = models.DateTimeField(blank=True,null=True)
    # phone_number_verify = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff_property(self):
        return self.is_staff
    
