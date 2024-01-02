from django.contrib import admin
from .models import Habit, HabitCompletion, DayOfWeek
from .forms import HabitForm
from django import forms


class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

class HabitAdmin(admin.ModelAdmin):
    list_display = ('name','id','user','get_days_of_week')

    def get_days_of_week(self, obj):
        return ", ".join([day.name for day in obj.days_of_week.all()])

    get_days_of_week.short_description = 'Days of Week'



admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitCompletion)
admin.site.register(DayOfWeek, DayOfWeekAdmin)
