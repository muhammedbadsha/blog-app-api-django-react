from django.urls import path
from .import views

urlpatterns = [
    path('', views.HomePage.as_view(),name='HomePage'),
    path('register', views.RegisterPage.as_view(),name='register'),
    
]
