from datetime import datetime
from rest_framework.serializers import ValidationError
from habits_tracker.models import Habit


class HabitValidator:
    def validate_time_for_execution(self, attrs):
        """Проверка времени выполнения привычки."""
        if attrs["execution_time"] > 120:
            raise ValidationError("Время выполнения привычки не может быть больше 120 секунд!")

    def validate_related_habit(self, attrs):
        """Проверка связанной привычки на положительный статус приятной привычки."""
        if attrs.get("related_habit_id"):
            related_habit = Habit.objects.get(pk=attrs.get("related_habit_id"))
            if not related_habit.pleasent:
                raise ValidationError("Только приятные привычки могут быть связанными!")

    def validate_reward(self, attrs):
        """Проверка на одновременное присутсвие награды и связанной привычки."""
        if attrs.get("related_habits_id") and attrs.get("reward"):
            raise ValidationError(
                "Запрещено выбирать одновременно награду и связанную привычку! Выберите что-то одно."
            )

    def validate_pleasant_habit(self, attrs):
        """Проверка приятной привычки на начилие награды."""
        if attrs.get("pleasent") and any(
                [attrs.get("related_habits_id"), attrs.get("reward"), attrs.get("frequency"), attrs.get("time")]
        ):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения!"
            )
        if not attrs.get("pleasent") and not any(
            [
                all([attrs.get("reward"), attrs.get("frequency"), attrs.get("time")]),
                all([attrs.get("related_habits_id"), attrs.get("frequency"), attrs.get("time")]),
            ]
        ):
            raise ValidationError(
                "У полезной привчки должна быть награда или связанная привычка, "
                "а также она должна выполняться в определенное время."
            )

    def validate_end_time(self, attrs):
        """Проверка повторяющейся за один день привычки на признак присутствия времени окончания."""
        if attrs.get("frequency") and "x" in attrs.get("frequency") and not attrs.get("end_time"):
            raise ValidationError(
                "Для привычки, которая должна выполняться несколько раз в день, должно быть указано время окончания."
            )
        if attrs.get("frequency") and "x" not in attrs.get("frequency") and attrs.get("end_time"):
            raise ValidationError(
                "Время окончания должно быть выбрано только для привычек, выполняемых несколько раз в день."
            )
        if (
                attrs.get("end_time")
                and attrs.get("time")
                and datetime.fromisoformat(attrs.get("end_time")).date()
                != datetime.fromisoformat(attrs.get("time")).date()
        ):
            raise ValidationError("Начало и время окончания должно быть выбрано в течение 1 дня.")
        if attrs.get("end_time") and attrs.get("time") and attrs.get("end_time") <= attrs.get("time"):
            raise ValidationError("Время окончания не может быть раньше или равное временю начала.")

    def validate_days_of_week(self, attrs):
        """Проверка выбора конкретных дней недели, когда должна быть выполнена привычка."""
        if attrs.get("frequency") and "d" in attrs.get("frequency") and not attrs.get("days_of_week"):
            raise ValidationError(
                "Для привычки, которая должна быть выполнена в определенные дни недели, необходимо вырать дни."
            )
        if attrs.get("frequency") and "d" not in attrs.get("frequency") and attrs.get("days_of_week"):
            raise ValidationError(
                "Конкретные дни должны быть выбраны только для привычек, выполняемых в определенные дни."
            )

    def __call__(self, attrs):
        self.validate_time_for_execution(attrs)
        self.validate_related_habit(attrs)
        self.validate_reward(attrs)
        self.validate_pleasant_habit(attrs)
        self.validate_end_time(attrs)
        self.validate_days_of_week(attrs)
