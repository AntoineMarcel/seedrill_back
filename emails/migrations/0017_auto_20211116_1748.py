# Generated by Django 3.2.9 on 2021-11-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0016_auto_20211116_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequence',
            name='background_color',
            field=models.CharField(default='test', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequence',
            name='gain',
            field=models.CharField(default='test', max_length=150, verbose_name='Gain'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequence',
            name='message',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequence',
            name='promo_code',
            field=models.CharField(default='test', max_length=150, verbose_name='Promo Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequence',
            name='text_color',
            field=models.CharField(default='test', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequence',
            name='website',
            field=models.URLField(default='test.fr', verbose_name='Website'),
            preserve_default=False,
        ),
    ]
