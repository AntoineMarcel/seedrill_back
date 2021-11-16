import datetime
from django.utils.timezone import now
import uuid

from django.db import models
from ordered_model.models import OrderedModel
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User

class Sequence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    senderName = models.CharField("Name of the sender", max_length=150)
    subjectEmail = models.CharField("Subject of emails", max_length=150)
    replyEmail = models.EmailField("Email for reply-to")
    website = models.URLField("Website")
    promo_code = models.CharField("Promo Code", max_length=150)
    gain = models.CharField("Gain", max_length=150)
    background_color = models.CharField(max_length=60)
    text_color = models.CharField(max_length=60)
    message = models.CharField(max_length=200)

class EmailModel(OrderedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    days = models.PositiveIntegerField("Days before send", default=1, validators=[MinValueValidator(1), MaxValueValidator(30)])
    model = models.TextField("Model")

    order_with_respect_to = 'sequence'
    class Meta:
        ordering = ('order',)

    def modelise_email(self, person):
        email = self.model
        email = email.replace("{{firstName}}", person.firstName)
        email = email.replace("{{lastName}}", person.lastName)
        return email
# class Variable(models.Model):
#     sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
#     name = models.CharField("Nom", max_length=50)

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    nextStep = models.ForeignKey(EmailModel, on_delete=models.CASCADE,blank=True,null=True)
    nextStepDate = models.DateField("Next action date", blank=True,null=True)
    firstName = models.CharField("First name", max_length=50)
    lastName = models.CharField("Last name", max_length=50)
    email = models.EmailField()
    visits = models.IntegerField(default=0)
    buy = models.IntegerField(default=0)

    class Meta:
        unique_together = ("email", "sequence")

    def refresh_step(self):
        try:
            nextStep = EmailModel.objects.get(order=self.nextStep.order + 1)
            self.nextStep = nextStep
            self.nextStepDate = now().date() + datetime.timedelta(days=nextStep.days)
            self.save()
        except:
            self.nextStep = None
            self.nextStepDate = None
            self.save()