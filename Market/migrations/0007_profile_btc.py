# Generated by Django 5.0.8 on 2024-08-13 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_alter_userwallet_private_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='btc',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
