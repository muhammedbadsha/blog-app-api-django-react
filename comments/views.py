from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

class CommentView(APIView):
    def get(self, request,pk=None):
        pass