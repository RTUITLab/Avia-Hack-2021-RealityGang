from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class Message(models.Model):
    description = models.TextField('Описание', max_length=256)
    created_at = models.DateTimeField('Время публикации', default=datetime.now)
    status = models.CharField('Статус', default='Обработано', max_length=256)
    answer = models.FileField('answer', null=True)
    correct = models.FileField('correct', null=True)
    incorrect = models.FileField('incorrect', null=True)
    kml = models.FileField('kml', null=True)
    # json = models.CharField('JSON', default='', max_length=1000000)

    user = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='Пользователь',
                             related_name='messages', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка №{self.pk}'


class User(AbstractUser):
    full_name = models.CharField('Фамилия И.О.', max_length=50)

    # messages = models.ForeignKey('Message', on_delete=models.SET_NULL, verbose_name='Заявки',
    #                              related_name='user', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name
