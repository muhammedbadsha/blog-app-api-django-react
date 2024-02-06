from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogPostViews(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','user', 'about','body','conclusion','category']
