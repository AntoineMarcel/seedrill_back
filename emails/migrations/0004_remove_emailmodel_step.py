# Generated by Django 3.2.9 on 2021-11-07 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_auto_20211107_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailmodel',
            name='step',
        ),
    ]
