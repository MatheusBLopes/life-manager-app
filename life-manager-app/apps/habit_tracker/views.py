from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect

from .models import Habit, Day, Week, DayOfWeekChoice, HabitRecurrence, HabitSchedule

from django.views import View


def calculate_weeks_and_years(week_number, year):
    if 1 <= week_number <= 52:
        next_week = (week_number % 52) + 1
        previous_week = (week_number - 2) % 52 + 1
        previous_year = year - 1 if week_number == 1 else year
        next_year = year + 1 if week_number == 52 else year
    else:
        raise ValueError("Invalid week number. It should be between 1 and 52.")
    return previous_year, next_year, previous_week, next_week

@login_required
def habit_tracker(request, week_number=None, year=None):
    # Helper function for formatting dates
    def format_date(day):
        day.day_name = day.date.strftime("%A")
        day.formated_date = day.date.strftime("%d/%m/%Y")

    if week_number is None or year is None:
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_number = start_of_week.isocalendar()[1]
        year = today.year

    current_week, _ = Week.objects.get_or_create(week_number=week_number, year=year)

    week_days = current_week.day_set.all()

    for day in week_days:
        format_date(day)
        day.habit_schedules = HabitSchedule.objects.filter(day=day)


    previous_year, next_year, previous_week, next_week = calculate_weeks_and_years(current_week.week_number, current_week.year)

    return render(
        request,
        'habit_tracker/pages/week.html',
        context={
            "days": week_days,
            "week": {
                'previous_week': previous_week,
                'next_week': next_week,
                'current_week': current_week.week_number,
                'present_week': datetime.now().date().isocalendar()[1]
            },
            "previous_year": previous_year,
            "next_year": next_year,
            "current_year": year,
            "present_year": datetime.now().date().year,
        }
    )

def create_days_and_schedules(habit, habit_recurrence, db_days_of_week):
    start_date = datetime.strptime(habit_recurrence.start_date, "%Y-%m-%d")
    final_date = start_date + timedelta(days=365)
    selected_dates = []
    db_days_id_list = db_days_of_week.values_list('id', flat=True)
    current_date = start_date
    #TODO: atualizar o modelo para iniciar a contagem com 0 na segunda feira
    days_dict = {
        6:1,
        0:2,
        1:3,
        2:4,
        3:5,
        4:6,
        5:7,
    }

    # Loop through dates until reaching the end date
    while current_date <= final_date:
        # Check if the current date's day of the week is in the selected days
        if days_dict[current_date.weekday()] in db_days_id_list:
            selected_dates.append(current_date)

        # Move to the next day
        current_date += timedelta(days=1)
    
    for date in selected_dates:
        Week.objects.get_or_create(week_number=date.isocalendar()[1], year=date.year)

    days_to_schedule = Day.objects.filter(date__in=selected_dates)

    for day in days_to_schedule:
        HabitSchedule.objects.create(habit=habit, day=day)

@login_required
def create_habit(request):
    if request.method == 'POST':
        # Accessing the selected habit ID
        habit_name = request.POST.get('habit_name', None)
        
        habit = Habit.objects.create(name=habit_name, user=request.user)

        form_days_of_week = request.POST.getlist('day_of_week')
        db_days_of_week = DayOfWeekChoice.objects.filter(day_of_week__in=form_days_of_week)

        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)

        if not end_date:
            end_date = None


        habit_recurrence = HabitRecurrence.objects.create(habit=habit, start_date=start_date, end_date=end_date)
        habit_recurrence.days_of_week.add(*db_days_of_week)
        habit_recurrence.save()

        #TODO: Criar apenas os schedules da semana corrente, o restante criar conforme as semanas forem mostradas na tela
        create_days_and_schedules(habit, habit_recurrence, db_days_of_week)

        return HttpResponseRedirect(reverse('habit_tracker:habit_tracker'))
    else:
        habits = Habit.objects.all()

    return render(
        request, 
        'habit_tracker/pages/create-habit.html', 
        context={
            'habits': habits
        }
    )


class MarkCompletedView(View):

    def post(self, request, *args, **kwargs):
        habit_schedule_id = request.POST.get('habit_schedule_id')

        habit_schedule = HabitSchedule.objects.get(id=habit_schedule_id)

        if habit_schedule:
            completion_status = request.POST.get('completion_status', None)
            description = request.POST.get('description', None)

            habit_schedule.completion_status = completion_status
            habit_schedule.description = description

            habit_schedule.save()

        return redirect('habit_tracker:habit_tracker', week_number=kwargs['week'], year=kwargs['year'])