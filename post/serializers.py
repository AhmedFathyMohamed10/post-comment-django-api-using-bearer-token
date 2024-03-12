from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Posts, Comment

class PostSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = ('title', 'content')

        extra_kwargs = {
            'title': {'required':True ,'allow_blank':False},
            'content' : {'required':True ,'allow_blank':False}
        }


class CommentSerializer(ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    
    def create(self, validated_data):
        post = self.context['post']
        comment = Comment.objects.create(post=post, **validated_data)
        return comment
    
    class Meta:
        model = Comment
        fields = ('comment', 'post')

        extra_kwargs = {
            'comment': {'required':True ,'allow_blank':False}
        }