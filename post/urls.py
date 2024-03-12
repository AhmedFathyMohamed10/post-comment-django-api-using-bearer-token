from django.urls import path
from . import views

urlpatterns = [
    path('create-post/', views.createPost, name='create-post'),
    path('post-info/<str:pk>/', views.gePost, name='post-info'),
    path('post-info/<str:pk>/update', views.updatePost, name='post-info-update'),
    path('post-info/<str:pk>/delete', views.delete_post, name='post-info-delete'),
    path('<str:post_id>/create-comment/', views.createComment, name='create-comment'),
]