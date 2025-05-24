from django.shortcuts import get_object_or_404
from django_celery_beat.models import PeriodicTask
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits_tracker.models import Habit
from habits_tracker.paginators import HabitPaginator
from habits_tracker.serializers import HabitSerializer, PublicHabitSerializer
from habits_tracker.services import create_replacements, make_replacements, create_schedule, create_task
from users.permissions import IsUser


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        if not habit.pleasent:
            replacements = create_replacements(habit)
            habit.frequency = make_replacements(habit.frequency, replacements)
            habit.save()

            if habit.user.telegram_id:
                schedule = create_schedule(habit.frequency)
                create_task(schedule, habit)


class PublicHabitListAPIView(ListAPIView):
    serializer_class = PublicHabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(publicity=True)


class HabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsUser,)


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsUser,)

    def perform_update(self, serializer):
        habit = serializer.save(user=self.request.user)

        if not habit.pleasent:
            replacements = create_replacements(habit)
            habit.frequency = make_replacements(
                habit.frequency, replacements
            )
            habit.save()

            if habit.user.telegram_id:
                task = get_object_or_404(PeriodicTask, name=f"Напоминаем о привычке {habit.pk}")
                schedule = create_schedule(habit.frequency)

                if task:
                    task.enabled = False
                    task.delete()
                create_task(schedule, habit)


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsUser,)
