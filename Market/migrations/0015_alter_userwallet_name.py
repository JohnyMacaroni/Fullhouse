# Generated by Django 5.0.8 on 2024-08-16 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0014_userwallet_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='name',
            field=models.CharField(default=models.CharField(max_length=255), max_length=512),
        ),
    ]
