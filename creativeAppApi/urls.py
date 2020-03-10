from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/', include('accounts.api.urls')),
    url('api/showcase/', include('showcase.api.urls')),
    url('api/collaboration/', include('collaborate.api.urls')),
]
