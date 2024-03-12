# Post-Comment Django API using Bearer Token Authentication

This is a Django REST Framework (DRF) API for managing posts and comments. It provides endpoints for creating, retrieving, updating, and deleting posts and comments.

## Features

- Create, read, update, and delete posts.
- Create, read comments on posts.
- Bearer token authentication for user authorization.
- Customizable permissions and authentication classes.

## Authentication
The API uses bearer token authentication for user authorization. To obtain a token:

- Register a new user using the /api/register/ endpoint.

- Obtain an access token by sending a POST request to the /api/token/ endpoint with the user's credentials.

- Use the obtained access token in the Authorization header of subsequent requests as follows:
    Authorization: Bearer <access_token>

## Testing Models
    Test that the models behave as expected, including field constraints, relationships, and any custom methods.
    
## Testing Serializers
    Test that the serializers correctly serialize and deserialize data, including validation rules and field exclusion.

## API Endpoints
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/post/', include('post.urls')),
    path('api/token-obtain/', TokenObtainPairView.as_view()),
    path('register/', registerUser, name='register'),
    path('user-info/', get_user, name='user-info'), 
    path('users/', get_users, name='users'), 
    path('user-update/', update_user_info, name='user-update'), 
    path('user-delete/', delete_my_account, name='user-delete'), 
    path('forget-password/', forgot_password, name='forget-pass'), 
    path('reset_password/<str:token>', reset_password, name='reset-pass'), 
    path('create-post/', views.createPost, name='create-post'),
    path('post-info/<str:pk>/', views.gePost, name='post-info'),
    path('post-info/<str:pk>/update', views.updatePost, name='post-info-update'),
    path('post-info/<str:pk>/delete', views.delete_post, name='post-info-delete'),
    path('<str:post_id>/create-comment/', views.createComment, name='create-comment')
