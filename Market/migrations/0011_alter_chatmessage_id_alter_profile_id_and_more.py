# Generated by Django 5.0.8 on 2024-08-14 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0010_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userwallet',
            name='id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False),
        ),
    ]
