from django.urls import path
from .views import Person_API, Emails_API, SendEmail_API,DeletePerson_API, Sequence_API, CreateSequence_API

urlpatterns = [
    path('sequence/', CreateSequence_API.as_view(), name="sequence"),
    path('sequence/<uuid:token>', Sequence_API.as_view()),
    path('person/<uuid:token>', Person_API.as_view()),
    path('person/<uuid:token>/<uuid:id>', DeletePerson_API.as_view()),
    path('emails/<uuid:token>', Emails_API.as_view()),
    path('send_email', SendEmail_API.as_view()),
]