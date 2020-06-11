# Generated by Django 3.0.5 on 2020-06-11 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0012_auto_20200611_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='username',
            field=models.ForeignKey(blank=True, db_column='username', null=True, on_delete=django.db.models.deletion.SET_NULL, to='iot.iotApp', to_field='username'),
        ),
    ]
