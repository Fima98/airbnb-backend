# Generated by Django 5.1.4 on 2025-03-19 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reservations',
            field=models.ManyToManyField(related_name='user_reservations', to='property.property'),
        ),
    ]
