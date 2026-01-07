"""Serializer for blog api"""

from rest_framework import serializers
from blog.models import Blog, BlogContentImage


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ["id", "name", "user" ,"content","created_at","thumbnail"]
        read_only_fields = ["id", "user","created_at"]


class BlogPostImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogContentImage
        fields = ["name", "image"]




