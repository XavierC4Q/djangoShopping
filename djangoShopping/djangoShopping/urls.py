from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'auth/register/', include('rest_auth.registration.urls')),
    url(r'^app/', include('app.urls')),
]
