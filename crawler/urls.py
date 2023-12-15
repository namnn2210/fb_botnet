from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, process

urlpatterns = [
    path('', index, name='index'),
    path('process/', process, name='process'),
]
