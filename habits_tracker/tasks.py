import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from habits_tracker.models import Habit


@shared_task
def send_message(pk) -> None:
    """Отправляет напоминание пользователю в Telegram."""
    habit = Habit.objects.get(pk=pk)
    text = (
        f"Веремя выполнить: {habit.action} в {habit.place}! "
        f"Награда за выполнение: {habit.reward if habit.reward else habit.related_habit}."
    )
    params = {
        "text": text,
        "chat_id": habit.user.telegram_id,
    }
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
