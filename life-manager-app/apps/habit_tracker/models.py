# habit_tracker/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Week(models.Model):
    year = models.PositiveIntegerField()
    week_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('year', 'week_number',)

    def __str__(self):
        return f"Week {self.week_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        existing_days = self.day_set.all()

        if not existing_days:
            jan4 = datetime(self.year, 1, 4)
            start_of_year_week = jan4 - timedelta(days=jan4.isoweekday() - 1)
            week_start = start_of_year_week + timedelta(weeks=self.week_number - 1)
            start_date = week_start - timedelta(days=(week_start.weekday() + 1) % 7)

            for i in range(7):
                date = start_date + timezone.timedelta(days=i)
                Day.objects.get_or_create(date=date, week=self)


class Day(models.Model):
    date = models.DateField(unique=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    habits = models.ManyToManyField('Habit', through='HabitSchedule', related_name='scheduled_habits')

    def __str__(self):
        return f"{self.date} - Week {self.week.week_number}"

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    goal = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class HabitRecurrence(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    days_of_week = models.ManyToManyField('DayOfWeekChoice', related_name='habit_recurrences')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.habit.name} recurrence on {', '.join(day.get_day_of_week_display() for day in self.days_of_week.all())}"

class DayOfWeekChoice(models.Model):
    day_of_week = models.CharField(max_length=10, choices=[
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])

    def __str__(self):
        return self.get_day_of_week_display()


class HabitSchedule(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    SUCCESS = 'success'
    FAILED = 'failed'
    NOT_COMPLETED = 'not_completed'

    COMPLETION_CHOICES = [
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (NOT_COMPLETED, 'Not Completed'),
    ]

    completion_status = models.CharField(
        max_length=15,
        choices=COMPLETION_CHOICES,
        default=NOT_COMPLETED,
    )

    description = models.TextField(blank=True, null=True)
    time_spent = models.DurationField(blank=True, null=True)

    class Meta:
        unique_together = ('habit', 'day',)

    def __str__(self):
        return f"{self.habit.name} scheduled for {self.day.date}"
