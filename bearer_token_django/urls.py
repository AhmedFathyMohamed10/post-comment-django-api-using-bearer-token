from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/post/', include('post.urls')),
    path('api/token-obtain/', TokenObtainPairView.as_view()),
]
