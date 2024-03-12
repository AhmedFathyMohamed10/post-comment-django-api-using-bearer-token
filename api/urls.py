from django.urls import path
from .views import registerUser, get_user, get_users, update_user_info, delete_my_account, forgot_password, reset_password

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('user-info/', get_user, name='user-info'), 
    path('users/', get_users, name='users'), 
    path('user-update/', update_user_info, name='user-update'), 
    path('user-delete/', delete_my_account, name='user-delete'), 
    path('forget-password/', forgot_password, name='forget-pass'), 
    path('reset_password/<str:token>', reset_password, name='reset-pass'), 

]