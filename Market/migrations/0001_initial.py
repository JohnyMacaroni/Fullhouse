# Generated by Django 4.0.6 on 2022-09-01 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Global_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneyin', models.IntegerField(default=0)),
                ('Totalcoins', models.IntegerField(default=0)),
                ('Totalprofit', models.IntegerField(default=0)),
                ('Players_online', models.IntegerField(default=0)),
                ('currency_value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Money', models.IntegerField(default=0)),
                ('Coins', models.IntegerField(default=0)),
                ('Profit', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=64)),
                ('message', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_username', models.CharField(blank=True, max_length=64, null=True)),
                ('Coins', models.PositiveIntegerField(default=0)),
                ('Price', models.PositiveIntegerField(default=0)),
                ('pp', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
