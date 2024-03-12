from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer, CommentSerializer
from .models import Posts, Comment
# ---------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data = request.data
    serializer = PostSerializer(data=data)

    if serializer.is_valid():
        post = serializer.save(user_id=request.user)
        return Response({
            'Details': serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            'Error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gePost(request, pk):
    post = get_object_or_404(Posts, id=pk)
    comments = post.comments.all()
    comments_count = comments.count()
    post_seializer = PostSerializer(post, many=False)
    comment_serializer = CommentSerializer(comments, many=True)
    return Response({
        'Post Details': post_seializer.data, 
        'Number of comments': comments_count,
        'Comments': comment_serializer.data
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePost(request, pk):
    post = get_object_or_404(Posts, id=pk)

    data = request.data
    serializer = PostSerializer(post, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'Updated': serializer.data
        })
    return Response({
        'Error Occurred': serializer.errors
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    
    try:
        post = Posts.objects.get(id=pk)
        post.delete()
        return Response({'detail': 'The post is deleted successfully.'})
    
    except Posts.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=404) 
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createComment(request, post_id):
    data = request.data
    post = get_object_or_404(Posts, id=post_id)
    serializer = CommentSerializer(data=data, context={'post': post})  # Pass post as context
    user = request.user

    try:
        if serializer.is_valid():
            # Save the comment along with the data
            comment = serializer.save(user=user)
            return Response({
                'Comment': serializer.data  # Include the serialized comment data in the response
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'Error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        return Response({
            'Error': f'IntegrityError: {e}'
        }, status=status.HTTP_400_BAD_REQUEST)