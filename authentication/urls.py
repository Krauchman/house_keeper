from django.urls import path, include
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('token/', auth_views.obtain_auth_token),
]
