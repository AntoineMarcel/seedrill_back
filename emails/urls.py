from django.urls import path
from .views import Person_API, Emails_API, SendEmail_API,DeletePerson_API, Sequence_API

urlpatterns = [
    path('sequence/', Sequence_API.as_view()),
    path('person/', Person_API.as_view()),
    path('person/<uuid:id>', DeletePerson_API.as_view()),
    path('emails/', Emails_API.as_view()),
    path('send_email', SendEmail_API.as_view()),
]