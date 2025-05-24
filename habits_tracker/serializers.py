from rest_framework import serializers

from habits_tracker.models import Habit
from habits_tracker.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [HabitValidator()]

    def to_internal_value(self, data):
        if self.instance:
            if not data.get("days_of week"):
                data["days_of_week"] = [day.pk for day in self.instance.days_of_week.all()]
            for field in self.fields.keys():
                if field not in data.keys():
                    data[field] = getattr(self.instance, field)
        return data


class PublicHabitSerializer(HabitSerializer):
    class Meta(HabitSerializer.Meta):
        model = Habit
        fields = ("action", "pleasent", "execution_time")
