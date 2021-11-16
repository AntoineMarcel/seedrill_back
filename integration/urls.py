# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from .views import Banner_API, Payment_API

urlpatterns = [
    path('banner/<str:sequenceID>/<str:friendCode>', Banner_API.as_view()),
    path('payment/<str:sequenceID>', Payment_API.as_view())
]