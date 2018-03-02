from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

urlpatterns =[
    path('admin/', admin.site.urls),
    url(r'', include('myapp.urls', namespace='myapp')),
    url(r'^users/', include('users.urls',namespace="users"))
]

