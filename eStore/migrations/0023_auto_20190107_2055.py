# Generated by Django 2.1.4 on 2019-01-07 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0022_city_pin_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pin_code',
            name='city',
        ),
        migrations.DeleteModel(
            name='Pin_code',
        ),
    ]
