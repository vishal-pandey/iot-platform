# Generated by Django 3.0.5 on 2020-06-11 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0004_auto_20200609_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='iotapp',
            name='pwd',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='iotapp',
            name='super',
            field=models.SmallIntegerField(default=0),
        ),
    ]
