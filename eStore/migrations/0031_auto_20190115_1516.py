# Generated by Django 2.1.4 on 2019-01-15 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0030_auto_20190109_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_billing_address',
            old_name='Company',
            new_name='company',
        ),
        migrations.RenameField(
            model_name='user_shipping_address',
            old_name='Company',
            new_name='company',
        ),
    ]
