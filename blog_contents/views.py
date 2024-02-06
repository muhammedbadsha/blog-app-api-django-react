from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny

# file imports inside of the project
from .serializers import BlogSerializer,BlogPostViews
from .models import Blog
# Create your views here.

class BlogView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticatedOrReadOnly,AllowAny]
        query_set = Blog.objects.all()
        serializer = BlogPostViews(query_set,many=True)
        return Response(serializer.data)

class BlogPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query_set = Blog.objects.all()
        serializer = BlogSerializer(query_set)
