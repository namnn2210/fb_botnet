from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, issue

urlpatterns = [
    path('', index, name='index'),
    path('issue/', issue, name='issue'),
]
