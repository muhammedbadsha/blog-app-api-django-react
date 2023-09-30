from django.urls import path
from .import views

urlpatterns = [
    path('', views.HomePage.as_view(),name='HomePage'),
    path('register', views.RegisterPage.as_view(),name='register'),
    path('verify_otp/<int:id>',views.VerifyEmailOTP.as_view(),name='verify_otp'),
    # path('user_detail_view/<int:id>',views.UserDetailPage.as_view(),name='user_detail_view'),
]
