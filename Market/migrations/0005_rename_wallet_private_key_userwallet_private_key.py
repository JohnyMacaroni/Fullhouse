# Generated by Django 5.0.8 on 2024-08-13 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_marketinfo_btc_price_userwallet'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userwallet',
            old_name='wallet_private_key',
            new_name='private_key',
        ),
    ]
