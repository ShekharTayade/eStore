# Generated by Django 2.1.4 on 2019-01-07 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0020_auto_20190107_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='country',
            field=models.ForeignKey(default='IND', on_delete=django.db.models.deletion.CASCADE, to='eStore.Country'),
            preserve_default=False,
        ),
    ]
