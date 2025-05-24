from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits_tracker.models import Habit, Day
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.good_habit = Habit.objects.create(
            pk=1,
            user=self.user,
            place="Place 1",
            time="2025-03-30T19:30:00+07:00",
            action="Action 1",
            pleasent=False,
            frequency="30 15 * * *",
            reward="Reward 1",
            execution_time=90,
            publicity=True,
        )
        self.pleasant_habit = Habit.objects.create(
            pk=2,
            user=self.user,
            place="Pleasant place 1",
            action="Pleasant action 1",
            pleasent=True,
            execution_time=30,
            publicity=False,
        )
        self.user2 = User.objects.create(email="user2@user.ru")
        self.pleasant_habit2 = Habit.objects.create(
            pk=3,
            user=self.user2,
            place="Pleasant place 2",
            action="Pleasant action 2",
            pleasent=True,
            execution_time=30,
            publicity=True,
        )
        self.pleasant_habit3 = Habit.objects.create(
            pk=4,
            user=self.user2,
            place="Pleasant place 3",
            action="Pleasant action 3",
            pleasent=True,
            execution_time=30,
            publicity=False,
        )
        self.mon = Day.objects.create(pk=1, day="Понедельник")
        self.tue = Day.objects.create(pk=2, day="Вторник")
        self.client.force_authenticate(user=self.user)

    def test_habit_create_good_habit_with_reward(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "frequency": "m h * * d",
            "reward": "Reward 2",
            "execution_time": 90,
            "days_of_week": [1, 2],
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 5)
        frequency = Habit.objects.get(place="Place 2").frequency
        self.assertEqual(frequency, "30 16 * * Понедельник,Вторник")

    def test_habit_create_good_habit_with_related_habit(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "frequency": "m h * * *",
            "related_habits_id": 2,
            "execution_time": 90,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 5)
        frequency = Habit.objects.get(place="Place 2").frequency
        self.assertEqual(frequency, "30 16 * * *")

    def test_habit_create_good_habit_execution_time_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "frequency": "m h * * *",
            "reward": "Reward 2",
            "execution_time": 125,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"),
                         ["Время выполнения привычки не может быть больше 120 секунд!"])

    def test_habit_create_good_habit_related_habit_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "frequency": "m h * * *",
            "related_habit_id": 1,
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"), ["Только приятные привычки могут быть связанными!"])

    def test_habit_create_good_habit_reward_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "frequency": "m h * * *",
            "reward": "Reward 2",
            "related_habits_id": 2,
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Запрещено выбирать одновременно награду и связанную привычку! Выберите что-то одно."],
        )

    def test_habit_create_good_habit_no_reward_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "frequency": "m h * * *",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "У полезной привчки должна быть награда или связанная привычка, "
                "а также она должна выполняться в определенное время."
            ],
        )

    def test_habit_create_good_habit_no_time_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "action": "Action 2",
            "pleasent": False,
            "frequency": "m h * * *",
            "reward": "Reward 2",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "У полезной привчки должна быть награда или связанная привычка, "
                "а также она должна выполняться в определенное время."
            ],
        )

    def test_habit_create_good_habit_no_frequency_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "У полезной привчки должна быть награда или связанная привычка, "
                "а также она должна выполняться в определенное время."
            ],
        )

    def test_habit_create_good_no_end_time_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Для привычки, которая должна выполняться несколько раз в день, должно быть указано время окончания."],
        )

    def test_habit_create_good_end_time_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "frequency": "m h * * *",
            "end_time": "2025-03-30T18:30:00+03:00",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Время окончания должно быть выбрано только для привычек, выполняемых несколько раз в день."],
        )

    def test_habit_create_good_end_time_and_start_time_not_in_the_same_day_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "end_time": "2025-03-31T18:30:00+03:00",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"),
                         ["Начало и время окончания должно быть выбрано в течение 1 дня."])

    def test_habit_create_good_end_time_earlier_than_start_time_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "end_time": "2025-03-30T12:30:00+03:00",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"),
                         ["Время окончания не может быть раньше или равное временю начала."])

    def test_habit_create_no_days_of_week_error_1(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "frequency": "m h * * d",
            "execution_time": 120,
            "publicity": False,
            "days_of_week": [],
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Для привычки, которая должна быть выполнена в определенные дни недели, необходимо вырать дни."],
        )

    def test_habit_create_no_days_of_week_error_2(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "frequency": "m h * * d",
            "execution_time": 120,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Для привычки, которая должна быть выполнена в определенные дни недели, необходимо вырать дни."],
        )

    def test_habit_create_no_days_of_week_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "pleasent": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "end_time": "2025-03-30T17:30:00+03:00",
            "execution_time": 120,
            "publicity": False,
            "days_of_week": [1],
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Конкретные дни должны быть выбраны только для привычек, выполняемых в определенные дни."],
        )

    def test_habit_create_pleasant_habit(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "pleasent": True,
            "execution_time": 90,
            "publicity": False,
        }
        request = self.client.post(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 5)
        frequency = Habit.objects.get(place="Pleasant place new").frequency
        self.assertEqual(frequency, "m h * * *")

    def test_habit_create_pleasant_habit_related_habit_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "pleasent": True,
            "execution_time": 90,
            "publicity": False,
            "related_habits_id": 2,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "У приятной привычки не может быть вознаграждения!"
            ],
        )

    def test_habit_create_pleasant_habit_reward_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "pleasent": True,
            "execution_time": 90,
            "publicity": False,
            "reward": "Pleasant reward new",
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "У приятной привычки не может быть вознаграждения!"
            ],
        )

    def test_habit_create_pleasant_habit_frequency_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "pleasent": True,
            "execution_time": 90,
            "publicity": False,
            "frequency": "m h */2 * *",
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "У приятной привычки не может быть вознаграждения!"
            ],
        )

    def test_habit_create_pleasant_habit_time_error(self):
        url = reverse("habits_tracker:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "pleasent": True,
            "execution_time": 90,
            "publicity": False,
            "time": "2025-03-30T17:30:00+03:00",
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "У приятной привычки не может быть вознаграждения!"
            ],
        )

    def test_habit_retrieve(self):
        url = reverse("habits_tracker:habit-detail", args=(self.good_habit.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("place"), "Place 1")
        self.assertEqual(response.get("user"), self.user.pk)

    def test_habit_retrieve_public_habit_error(self):
        url = reverse("habits_tracker:habit-detail", args=(self.pleasant_habit2.pk,))
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_retrieve_non_public_habit_error(self):
        url = reverse("habits_tracker:habit-detail", args=(self.pleasant_habit3.pk,))
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_list(self):
        url = reverse("habits_tracker:habit-list")
        request = self.client.get(url)
        response = request.json()
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "time": self.good_habit.time,
                        "place": self.good_habit.place,
                        "action": self.good_habit.action,
                        "pleasent": self.good_habit.pleasent,
                        "publicity": self.good_habit.publicity,
                        "execution_time": self.good_habit.execution_time,
                        "reward": self.good_habit.reward,
                        "frequency": self.good_habit.frequency,
                        "end_time": None,
                        "user": self.user.pk,
                        "related_habits": None,
                        "days_of_week": [],
                    },
                    {
                        "id": self.pleasant_habit.pk,
                        "time": self.pleasant_habit.time,
                        "place": self.pleasant_habit.place,
                        "action": self.pleasant_habit.action,
                        "pleasent": self.pleasant_habit.pleasent,
                        "publicity": self.pleasant_habit.publicity,
                        "execution_time": self.pleasant_habit.execution_time,
                        "reward": None,
                        "frequency": "m h * * *",
                        "end_time": None,
                        "user": self.user.pk,
                        "related_habits": None,
                        "days_of_week": [],
                    },
                ],
            },
        )

    def test_public_habit_list(self):
        url = reverse("habits_tracker:public-habit-list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            [
                {
                    "action": self.good_habit.action,
                    "pleasent": self.good_habit.pleasent,
                    "execution_time": self.good_habit.execution_time,
                },
                {
                    "action": self.pleasant_habit2.action,
                    "pleasent": self.pleasant_habit2.pleasent,
                    "execution_time": self.pleasant_habit2.execution_time,
                },
            ],
        )

    def test_habit_update(self):
        url = reverse("habits_tracker:habit-update", args=(self.good_habit.pk,))
        body = {
            "place": "Place new",
            "time": "2025-03-30T15:30:00+03:00",
            "action": "Action 1",
            "pleasent": False,
            "frequency": "m h * * *",
            "reward": "Reward 1",
            "execution_time": 90,
            "publicity": True,
        }
        request = self.client.patch(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("place"), "Place new")

    def test_habit_delete(self):
        url = reverse("habits_tracker:habit-delete", args=(self.good_habit.pk,))
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 3)
