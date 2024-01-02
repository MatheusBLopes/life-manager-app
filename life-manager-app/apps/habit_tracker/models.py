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

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date_completed = models.DateField()
