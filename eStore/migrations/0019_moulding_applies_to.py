# Generated by Django 2.1.4 on 2019-01-07 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eStore', '0018_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='moulding',
            name='applies_to',
            field=models.CharField(choices=[('P', 'Applies to Paper Only'), ('C', 'Applies to Canvas Only'), ('B', 'Applies to Paper and Canvas')], default='B', max_length=1),
        ),
    ]
