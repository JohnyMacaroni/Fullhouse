# Generated by Django 5.0.8 on 2024-08-13 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_rename_wallet_private_key_userwallet_private_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='private_key',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='userwallet',
            name='wallet_address',
            field=models.CharField(max_length=255),
        ),
    ]
