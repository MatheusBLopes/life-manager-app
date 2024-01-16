import pytest
from django.contrib.auth.models import User

from apps.habit_tracker.models import Day, Habit, HabitSchedule, Week


@pytest.mark.django_db
class TestWeekModel:
    def test_str_representation(self):
        week = Week(year=2022, week_number=1)
        assert str(week) == "Week 1"

    def test_save_method_creates_days(self):
        week = Week(year=2022, week_number=1)
        week.save()
        assert Day.objects.filter(week=week).count() == 7


@pytest.mark.django_db
class TestDayModel:
    def test_str_representation(self):
        week = Week(year=2022, week_number=1)
        day = Day(date="2022-01-01", week=week)
        assert str(day) == "2022-01-01 - Week 1"


@pytest.mark.django_db
class TestHabitModel:
    def test_str_representation(self):
        user = User.objects.create(username="testuser")
        habit = Habit(user=user, name="Exercise")
        assert str(habit) == "Exercise"


@pytest.mark.django_db
class TestHabitScheduleModel:
    def test_str_representation(self):
        user = User.objects.create(username="testuser")
        habit = Habit.objects.create(user=user, name="Exercise")
        week = Week.objects.create(year=2022, week_number=1)
        day = Day.objects.create(date="2022-01-01", week=week)
        habit_schedule = HabitSchedule(habit=habit, day=day)
        assert str(habit_schedule) == "Exercise scheduled for 2022-01-01"
