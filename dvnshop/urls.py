from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myshp.urls')),
    path('shop/', include('myshp.urls')),
    path('author/', include('myshp.urls')),
