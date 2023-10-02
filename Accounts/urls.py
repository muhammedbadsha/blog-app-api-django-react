from django.urls import path
from .import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'verify_otp',views.VerifyEmailOTP,basename='verify_otp')

urlpatterns = [
    path('', views.HomePage.as_view(),name='HomePage'),
    path('register', views.RegisterPage.as_view(),name='register'),
    path('user_detail_view/<int:id>',views.UserDetailPage.as_view(),name='user_detail_view'),
    path('login', views.LoginUser.as_view(),name='login'),
    
]
urlpatterns += router.urls