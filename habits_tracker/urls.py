from django.urls import path

from habits_tracker.apps import HabitsTrackerConfig
from habits_tracker.views import (HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView, HabitRetrieveAPIView,
                                  HabitUpdateAPIView, PublicHabitListAPIView)

app_name = HabitsTrackerConfig.name

urlpatterns = [
    path("habits/new/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("habits/public/", PublicHabitListAPIView.as_view(), name="public-habit-list"),
    path("habits/", HabitListAPIView.as_view(), name="habit-list"),
    path("habits/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-detail"),
    path("habits/<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("habits/<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit-delete"),
]
