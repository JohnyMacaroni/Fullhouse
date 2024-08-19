# Generated by Django 5.0.8 on 2024-08-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_profile_btc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='btc',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=10),
        ),
    ]
