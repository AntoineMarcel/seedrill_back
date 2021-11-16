from django.urls import path
from .views import UserRecordView
from rest_framework.authtoken import views

urlpatterns = [
    path('user/', UserRecordView.as_view(), name='users'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]