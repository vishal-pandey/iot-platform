# Generated by Django 3.0.5 on 2020-06-11 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0009_auto_20200611_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='name',
            field=models.CharField(default='name', max_length=255),
            preserve_default=False,
        ),
    ]
