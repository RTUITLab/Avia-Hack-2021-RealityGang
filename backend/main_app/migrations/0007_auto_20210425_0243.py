# Generated by Django 3.2 on 2021-04-24 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_message_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='json',
        ),
        migrations.AddField(
            model_name='message',
            name='answer',
            field=models.FileField(null=True, upload_to='', verbose_name='Ответ'),
        ),
    ]
