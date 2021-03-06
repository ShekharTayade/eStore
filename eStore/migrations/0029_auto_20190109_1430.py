# Generated by Django 2.1.4 on 2019-01-09 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0028_auto_20190108_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_staus',
            field=models.CharField(blank=True, default='AC', max_length=2),
        ),
        migrations.AddField(
            model_name='order',
            name='discount_amt',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_staus',
            field=models.CharField(blank=True, default='PP', max_length=2),
        ),
    ]
