"""Serializer for blog api"""
import os
import uuid
from rest_framework import serializers
from blog.models import Blog, BlogContentImage


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Blog
        fields = ["id", "name", "user" ,"content","created_at","thumbnail","summary","category"]
        read_only_fields = ["id","summary","category","user","created_at"]


class BlogPostImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlogContentImage
        fields = ["name", "image"]
        read_only_fields = ["name"]

    def create(self, validated_data):
        image = validated_data.pop('image')
        ext = os.path.splitext(image.name)[1]
        name = f"{uuid.uuid4()}{ext}"
        
        # Manually create the instance
        instance = BlogContentImage.objects.create(name=name, image=image)
        return instance




