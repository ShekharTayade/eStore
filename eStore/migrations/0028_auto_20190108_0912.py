# Generated by Django 2.1.4 on 2019-01-08 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0027_auto_20190107_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion_product_tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=2000)),
                ('tag_url', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='product_product_tag',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product_product_tag',
            name='product_tag',
        ),
        migrations.AlterUniqueTogether(
            name='product_tag',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='product_tag',
            name='store',
        ),
        migrations.RemoveField(
            model_name='cart_item',
            name='product_product_tag',
        ),
        migrations.RemoveField(
            model_name='order_items',
            name='product_product_tag',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='product_tag',
        ),
        migrations.DeleteModel(
            name='Product_product_tag',
        ),
        migrations.DeleteModel(
            name='Product_tag',
        ),
        migrations.AddField(
            model_name='promotion_product_tag',
            name='promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eStore.Promotion'),
        ),
    ]
