# Generated by Django 3.2.9 on 2021-11-07 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0004_remove_emailmodel_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emails.emailmodel'),
        ),
    ]
