# Generated by Django 2.1.4 on 2019-01-16 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0034_auto_20190116_1216'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pin_code',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='pin_code',
            name='city',
        ),
    ]
