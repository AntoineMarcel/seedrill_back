# Generated by Django 3.2.9 on 2021-11-16 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0015_auto_20211107_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='buy',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='person',
            name='visits',
            field=models.IntegerField(default=0),
        ),
    ]
