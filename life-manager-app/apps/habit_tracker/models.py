# habit_tracker/models.py
from django.db import models
from django.contrib.auth.models import User

class DayOfWeek(models.Model):
    DAY_CHOICES = [
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
    ]

    name = models.CharField(max_length=3, choices=DAY_CHOICES)

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    days_of_week = models.ManyToManyField(DayOfWeek, related_name='habits')

    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class HabitCompletion(models.Model):
    SUCCESS = 'success'
    FAILED = 'failed'
    NOT_COMPLETED = 'not_completed'

    COMPLETION_CHOICES = [
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (NOT_COMPLETED, 'Not Completed'),
    ]


    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    creation_date = models.DateField()

    date_completed = models.DateField(blank=True, null=True)

    completion_status = models.CharField(
        max_length=15,
        choices=COMPLETION_CHOICES,
        default=NOT_COMPLETED,
    )

    description = models.TextField(blank=True, null=True)
    time_spent = models.DurationField(blank=True, null=True)

    class Meta:
        unique_together = ('habit', 'creation_date',)
