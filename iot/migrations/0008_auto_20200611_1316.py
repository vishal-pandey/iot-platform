# Generated by Django 3.0.5 on 2020-06-11 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0007_auto_20200611_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iotapp',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('rw', models.SmallIntegerField(default=1)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot.iotApp', to_field='username')),
            ],
        ),
    ]
