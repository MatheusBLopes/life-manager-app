from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Habit
from .forms import HabitForm
from django.db.models import Q, F

def get_start_date_from_week(year, week_number):
    jan4 = datetime(year, 1, 4)
    start_of_year_week = jan4 - timedelta(days=jan4.isoweekday() - 1)
    week_start = start_of_year_week + timedelta(weeks=week_number - 1)
    return week_start

def get_days_data(date, user):
    start_date = date - timedelta(days=date.weekday() + 1)

    days = []

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        day_name = current_date.strftime("%A")

        current_date_str = current_date.isoformat()
        
        # Filter habits based on day, start date, and end date (considering null or blank)
        # Filter habits based on day, start date, and end date
        habits_with_desired_day = Habit.objects.filter(
            Q(days_of_week__name=day_name[0:3]) &
            Q(user=user) &
            (Q(start_date__lte=current_date) & 
            (Q(end_date__gte=current_date) | Q(end_date__isnull=True))
        ))

        days.append({
            "date": current_date.strftime("%d/%m/%Y"),
            "day_name": day_name,
            "habits": habits_with_desired_day
        })

    return days

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
    if week_number is None or year is None:
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_number = start_of_week.isocalendar()[1]
    else:
        week_start = get_start_date_from_week(year, week_number)
        today = week_start

    days = get_days_data(today, request.user)
    previous_year, next_year, previous_week, next_week = calculate_weeks_and_years(week_number, today.year)

    return render(
        request,
        'habit_tracker/pages/week.html',
        context={
            "days": days,
            "week": {
                'previous_week': previous_week,
                'next_week': next_week
            },
            "previous_year": previous_year,
            "next_year": next_year
        }
    )

@login_required
def create_habit(request):
    if request.method == 'POST':
        habit_form = HabitForm(request.POST, user=request.user)
        if habit_form.is_valid():
            habit_form.save()
            return redirect(reverse('habit_tracker:habit_tracker'))
    else:
        habit_form = HabitForm(user=request.user)

    return render(request, 'habit_tracker/pages/create-habit.html', {'habit_form': habit_form})
