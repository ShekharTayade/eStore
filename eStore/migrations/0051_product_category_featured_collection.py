# Generated by Django 2.1.4 on 2019-02-05 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0050_auto_20190205_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_category',
            name='featured_collection',
            field=models.BooleanField(default=False),
        ),
    ]
