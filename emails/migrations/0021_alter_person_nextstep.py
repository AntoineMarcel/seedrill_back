# Generated by Django 3.2.9 on 2021-11-18 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0020_alter_person_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nextStep',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='emails.emailmodel'),
        ),
    ]
