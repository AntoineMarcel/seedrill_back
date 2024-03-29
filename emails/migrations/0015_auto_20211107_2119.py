# Generated by Django 3.2.9 on 2021-11-07 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0014_auto_20211107_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nextStep',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emails.emailmodel'),
        ),
        migrations.AlterField(
            model_name='person',
            name='nextStepDate',
            field=models.DateField(blank=True, null=True, verbose_name='Next action date'),
        ),
    ]
