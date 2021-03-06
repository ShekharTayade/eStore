# Generated by Django 2.1.4 on 2019-02-05 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eStore', '0051_product_category_featured_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, default='', max_length=40)),
                ('image_to_frame', models.ImageField(blank=True, default='', upload_to='uploads/%Y/%m/%d/')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('cart_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='eStore.Cart_item')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
