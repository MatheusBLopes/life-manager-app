from django.contrib import admin
from .models import Habit, Day, Week, HabitSchedule, HabitRecurrence, DayOfWeekChoice



class WeekAdmin(admin.ModelAdmin):
    list_display = ('id','week_number',)

class DayAdmin(admin.ModelAdmin):
    list_display = ('id','date',)

class HabitAdmin(admin.ModelAdmin):
    list_display = ('name','id','user')


admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitSchedule)
admin.site.register(HabitRecurrence)
admin.site.register(Week, WeekAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(DayOfWeekChoice)
