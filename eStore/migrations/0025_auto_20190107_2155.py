# Generated by Django 2.1.4 on 2019-01-07 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0024_auto_20190107_2057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_billing_address',
            old_name='used_latest',
            new_name='pref_addr',
        ),
        migrations.RenameField(
            model_name='user_shipping_address',
            old_name='used_latest',
            new_name='pref_addr',
        ),
        migrations.RemoveField(
            model_name='order_billing',
            name='address_3',
        ),
        migrations.RemoveField(
            model_name='order_billing',
            name='bill_to',
        ),
        migrations.RemoveField(
            model_name='order_shipping',
            name='address_3',
        ),
        migrations.RemoveField(
            model_name='order_shipping',
            name='ship_to',
        ),
        migrations.RemoveField(
            model_name='user_billing_address',
            name='address_3',
        ),
        migrations.RemoveField(
            model_name='user_billing_address',
            name='bill_to',
        ),
        migrations.RemoveField(
            model_name='user_shipping_address',
            name='address_3',
        ),
        migrations.RemoveField(
            model_name='user_shipping_address',
            name='ship_to',
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cart_item',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order_billing',
            name='Company',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='order_billing',
            name='billing_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order_billing',
            name='full_name',
            field=models.CharField(default='Test_user', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_billing',
            name='land_mark',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='order_billing',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order_items',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='Company',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='full_name',
            field=models.CharField(default='Test_user', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='land_mark',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order_shipping_status_log',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_billing_address',
            name='Company',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='user_billing_address',
            name='full_name',
            field=models.CharField(default='Test_user', max_length=600),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_billing_address',
            name='land_mark',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='user_billing_address',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user_shipping_address',
            name='Company',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='user_shipping_address',
            name='full_name',
            field=models.CharField(default='Test_user', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_shipping_address',
            name='land_mark',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AddField(
            model_name='user_shipping_address',
            name='updated_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order_billing',
            name='address_1',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='order_billing',
            name='address_2',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='order_billing',
            name='city',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='order_billing',
            name='country',
            field=models.ForeignKey(default='IND', on_delete=django.db.models.deletion.PROTECT, to='eStore.Country'),
        ),
        migrations.AlterField(
            model_name='order_billing',
            name='pin_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eStore.Pin_code'),
        ),
        migrations.AlterField(
            model_name='order_shipping',
            name='address_1',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='order_shipping',
            name='address_2',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='order_shipping',
            name='city',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='order_shipping',
            name='country',
            field=models.ForeignKey(default='IND', on_delete=django.db.models.deletion.PROTECT, to='eStore.Country'),
        ),
        migrations.AlterField(
            model_name='order_shipping',
            name='pin_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eStore.Pin_code'),
        ),
        migrations.AlterField(
            model_name='user_billing_address',
            name='address_1',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='user_billing_address',
            name='address_2',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='user_billing_address',
            name='city',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='user_billing_address',
            name='country',
            field=models.ForeignKey(default='IND', on_delete=django.db.models.deletion.PROTECT, to='eStore.Country'),
        ),
        migrations.AlterField(
            model_name='user_billing_address',
            name='pin_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eStore.Pin_code'),
        ),
        migrations.AlterField(
            model_name='user_billing_address',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eStore.State'),
        ),
        migrations.AlterField(
            model_name='user_shipping_address',
            name='address_1',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='user_shipping_address',
            name='address_2',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
        migrations.AlterField(
            model_name='user_shipping_address',
            name='city',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='user_shipping_address',
            name='country',
            field=models.ForeignKey(default='IND', on_delete=django.db.models.deletion.PROTECT, to='eStore.Country'),
        ),
        migrations.AlterField(
            model_name='user_shipping_address',
            name='pin_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eStore.Pin_code'),
        ),
        migrations.AlterField(
            model_name='user_shipping_address',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eStore.State'),
        ),
    ]
