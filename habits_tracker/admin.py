from django.contrib import admin
from habits_tracker.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Habit._meta.fields]
