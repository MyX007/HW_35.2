from django.db import models
from config.settings import HABIT_FREQUENCY

from users.models import User


class Day(models.Model):
    day = models.CharField(max_length=100, unique=True, verbose_name="День недели", null=True, blank=True)


class Habit(models.Model):
    """Класс привычки."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='habits',
                             null=True, blank=True)
    time = models.DateTimeField(verbose_name='Время', null=True, blank=True)
    place = models.CharField(max_length=50, verbose_name='Место', null=True, blank=True)
    action = models.CharField(max_length=50, verbose_name='Действие', null=True, blank=True)
    pleasent = models.BooleanField(verbose_name='Признак приятной привычки', default=False)
    publicity = models.BooleanField(verbose_name='Признак публичности', default=False)
    execution_time = models.PositiveIntegerField(default=0, verbose_name='Время на выполнение')
    reward = models.CharField(max_length=50, verbose_name='Награда', blank=True, null=True)
    related_habits = models.ForeignKey(
        'self',
        verbose_name='Связанная привычка',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    frequency = models.CharField(
        max_length=50,
        choices=HABIT_FREQUENCY,
        verbose_name="frequency",
        default="m h * * *",
        blank=True,
        null=True,
    )
    days_of_week = models.ManyToManyField(
        Day,
        null=True,
        blank=True,
        verbose_name="День недели"
    )
    end_time = models.DateTimeField(
        verbose_name="Время последнего выполнения привычки за день",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
