# Generated by Django 3.0.5 on 2020-06-11 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0008_auto_20200611_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='username',
            field=models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, to='iot.iotApp', to_field='username'),
        ),
    ]