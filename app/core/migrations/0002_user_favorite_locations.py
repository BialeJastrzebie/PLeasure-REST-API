# Generated by Django 4.0.10 on 2024-05-26 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_locations',
            field=models.ManyToManyField(related_name='favorite_locations', to='core.location'),
        ),
    ]
