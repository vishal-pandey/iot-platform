# Generated by Django 3.0.5 on 2020-06-09 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0003_iotapp_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='iotapp',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='iotapp',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
