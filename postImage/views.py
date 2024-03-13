from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import PostWithImage
from .serializers import PostWithImageSerializer

from django.shortcuts import get_object_or_404

class PostWithImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        user = request.user
        serializer = PostWithImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user = user)
            return Response({
                'status': 'Post uploaded successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'Cannot upload the Post!',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PostList(APIView):
    def get(self, request, format=None):
        posts = PostWithImage.objects.all()
        serializer = PostWithImageSerializer(posts, many=True)
        return Response(serializer.data)
    

class GetPost(APIView):
    def get(self, request, pk, format=None):
        post = get_object_or_404(PostWithImage, id=pk)
        serializer = PostWithImageSerializer(post, many=False)
        return Response({
            'Data': serializer.data
        }, status=status.HTTP_200_OK)
    

class UpdatePostView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        post = get_object_or_404(PostWithImage, id=pk)
        data = request.data
        user = request.user
    
        if post.user != user:
            return Response({
                'Permission denied': "You don't have permission to update this post!"
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostWithImageSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'Updated': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        post = get_object_or_404(PostWithImage, id=pk)
        user = request.user

        if post.user != user:
            return Response({
                'Permission denied': "You don't have permission to delete this post!"
            }, status=status.HTTP_403_FORBIDDEN)
        
        else:
            post.delete()
            return Response({
                'Deleted': "Post deleted successfully"
            }, status=status.HTTP_202_ACCEPTED)
        