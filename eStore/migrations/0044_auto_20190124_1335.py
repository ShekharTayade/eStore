# Generated by Django 2.1.4 on 2019-01-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0043_auto_20190124_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='voucher_disc_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='order',
            name='vouncher_disc_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
