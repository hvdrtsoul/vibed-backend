from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api/', include('streaming.urls')),
    path('auth/', include('phantom_auth.urls')),
]
