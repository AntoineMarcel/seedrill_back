import datetime
from django.utils.timezone import now
from rest_framework import response, status

from emails.serializers import PersonSerializer
from .models import EmailModel, Person
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def replace_variable(message, person):
    message = message.replace("{{firstName}}", person.firstName)
    message = message.replace("{{lastName}}", person.lastName)
    return message

def create_lead(request, sequence):
    step = EmailModel.objects.filter(sequence=sequence).order_by("order").first()
    nextStepDate = now().date() + datetime.timedelta(days=step.days)
    step_id = step.id
    serializer_list = []
    for newPerson in request.data["data"]:
        newPerson["sequence"] = sequence
        newPerson["nextStep"] = step_id
        newPerson["nextStepDate"] = nextStepDate
        serializer = PersonSerializer(data=newPerson)
        if not serializer.is_valid():
            return response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer_list.append(serializer)
    for serializer in serializer_list:
        serializer.save()

def send_mailModel(person:Person):
    content = replace_variable(person.nextStep.model, person)
    subjectEmail = person.sequence.subjectEmail
    senderName = person.sequence.senderName
    replyEmail = person.sequence.replyEmail
    
    email = EmailMessage(
        subjectEmail,
        content,
        senderName + '<saveurdinde@gmail.com>',
        [person.email],
        reply_to=[replyEmail],
    )

    email.send()

