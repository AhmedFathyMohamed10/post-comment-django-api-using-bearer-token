from django.urls import path
from .views import PostWithImageView, PostList, GetPost, UpdatePostView, DeletePostView

urlpatterns = [
    path('create/', PostWithImageView.as_view(), name='post_with_image'),
    path('get-posts/', PostList.as_view(), name='get-posts'),
    path('post/<str:pk>/', GetPost.as_view(), name='get-post'),
    path('update-post/<str:pk>/', UpdatePostView.as_view(), name='update-post'),
    path('delete-post/<str:pk>/', DeletePostView.as_view(), name='delete-post'),
]
