# Generated by Django 3.0.5 on 2020-06-29 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0015_plan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='plan',
            new_name='name',
        ),
    ]
