# Generated by Django 5.0.8 on 2024-08-16 21:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0013_profile_id_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwallet',
            name='name',
            field=models.CharField(default=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), max_length=512),
        ),
    ]
