# Generated by Django 3.2.9 on 2021-11-16 19:55

from django.db import migrations, models
import emails.models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0018_sequence_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='friendCode',
            field=models.CharField(default=emails.models.RandomID, editable=False, max_length=6, unique=True),
        ),
    ]