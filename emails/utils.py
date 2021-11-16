from .models import Person
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def send_mailModel(person:Person):
    content = person.nextStep.modelise_email(person)
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

