from rest_framework import serializers
from .models import PostWithImage

class PostWithImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostWithImage
        fields = ['title', 'content', 'image', 'created_at']