from datetime import datetime, timedelta

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from .serializers import SignUpSerializer, UserSerializer
from post.serializers import PostSerializer
from post.models import Posts
# Create your views here.


@api_view(['POST'])
def registerUser(request):
    data = request.data
    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'], 
                email = data['email'] , 
                username = data['username'] , 
                password = make_password(data['password']),
            )
            return Response({
                'Details': 'Your Account has been created successfully!'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'Error': 'This credienials already exists!!'
            }, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({
            'Error': user.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_user(request):
    user = request.user
    posts = user.posts.all()
    serializer = UserSerializer(user, many=False)
    post_serializer = PostSerializer(posts, many=True)

    return Response({
        'Details of the User': serializer.data,
        'User posts': post_serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response({
        'Details': serializer.data
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):

    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']

    password = data['password']
    if password == "":
        return Response({
            'Error': 'password cannot be empty! try again'
        })
    elif len(password) < 8: 
        return Response({
            'Error': 'password cannot be less than 8 characters! try again'
        })
    else:
        user.password = make_password(password)

    user.save()
    return Response({
        'Details': 'Update of the information has been successfully changed.'
    })

     
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_my_account(request):
    user = request.user
    if user.is_staff == False:
        return Response({
            'Details': 'You cannot delete the account!!'
        })
    else:
        user.delete()
        return Response({
            'Details of deletion': 'Account has been deleted successfully.'
        })
    

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}".format(protocol=protocol, host=host)


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User,email=data['email'])

    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)

    user.profile.reset_password_token = token
    user.profile.forgot_password_expire = expire_date
    user.profile.save()
    
    host = get_current_host(request)
    link = "{host}/api/reset_password/{token}".format(host=host, token=token)
    body = "Your password reset link is : {link}".format(link=link)

    send_mail(
        "Paswword reset from eMarket",
        body,
        "admin@gmail.com",
        [data['email']]
    )

    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})

 
@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile and user.profile.forgot_password_expire:
        if user.profile.forgot_password_expire.replace(tzinfo=None) < datetime.now():
            return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Forgot password expiry not set'}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(data['password'])  # set_password instead of directly assigning
    user.save()

    user.profile.reset_password_token = ""
    user.profile.forgot_password_expire = None
    user.profile.save()

    return Response({'details': 'Password reset done'})