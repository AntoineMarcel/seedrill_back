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

def replace_variable(message, person:Person):
    message = message.replace("{{firstName}}", person.firstName)
    message = message.replace("{{lastName}}", person.lastName)
    message = message.replace("{{friendCode}}", person.friendCode)
    message = message.replace("{{promo_code}}", person.sequence.promo_code)
    message = message.replace("{{gain}}", person.sequence.gain)
    message = message.replace("{{friendLink}}", person.sequence.website + "?friendCode=" + person.friendCode)
    return message

def create_lead(data, sequence):
    emails = EmailModel.objects.filter(sequence=sequence.id)
    if (len(emails) <= 0):
        return {"status": "error", "data": "no email in your sequence"}
    step = EmailModel.objects.filter(sequence=sequence).order_by("order").first()
    nextStepDate = now().date() + datetime.timedelta(days=step.days)
    step_id = step.id
    serializer_list = []
    for newPerson in data["data"]:
        newPerson["sequence"] = sequence.id
        newPerson["nextStep"] = step_id
        newPerson["nextStepDate"] = nextStepDate
        serializer = PersonSerializer(data=newPerson)
        if not serializer.is_valid():
            return {"status": "error", "data": serializer.errors}
        serializer_list.append(serializer)
    for serializer in serializer_list:
        serializer.save()
    return {"status": "success", "data": "Persons added"}

def send_mailModel(person:Person):
    content = replace_variable(person.nextStep.model, person)
    subjectEmail = replace_variable(person.sequence.subjectEmail, person)
    senderName = person.sequence.senderName
    replyEmail = person.sequence.replyEmail
    email = EmailMessage(
        subjectEmail,
        content,
        senderName + ' <friend@seedrill.co>',
        [person.email],
        reply_to=[replyEmail],
    )

    email.send()

