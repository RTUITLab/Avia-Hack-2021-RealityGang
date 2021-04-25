# Generated by Django 3.2 on 2021-04-24 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210424_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='messages',
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
