from django.urls import path
from .views import hello_world, author, shop

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('author/', author, name='author'),
    path('shop/', shop, name='shop'),
]