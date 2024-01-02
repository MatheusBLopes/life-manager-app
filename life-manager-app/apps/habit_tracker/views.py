from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Habit
from .forms import HabitForm


def get_start_date_from_week(year, week_number):
    # January 4th is always in week 1 according to ISO standard
    jan4 = datetime(year, 1, 4)

    # Find the Monday of the week containing January 4th
    start_of_year_week = jan4 - timedelta(days=jan4.isoweekday() - 1)

    # Calculate the start date of the given week number
    week_start = start_of_year_week + timedelta(weeks=week_number - 1)

    return week_start

def get_days_data(date, user):
    # Calculate the most recent Sunday
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
    start_date = date - timedelta(days=date.weekday() + 1)

    # Generate dates for the week starting from Sunday
    days = []
    for i in range(7):
        date = start_date + timedelta(days=i)
        day_name = date.strftime("%A")  # Get the day name (e.g., Sunday, Monday)

        # Define habits for each day
        habits_with_desired_day = Habit.objects.filter(days_of_week__name=day_name[0:3])
        user_habits_with_desired_day = habits_with_desired_day.filter(user=user)

        # Append the day's info to the days list
        days.append({
            "date": date.strftime("%d/%m/%Y"),
            "day_name": day_name,  # Add the day name to the dict
            "habits": user_habits_with_desired_day
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

    # Render the template with the days context
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
            return redirect(reverse('habit_tracker:habit_tracker'))  # Redirect to a success page
    else:
        habit_form = HabitForm(user=request.user)

    return render(request, 'habit_tracker/pages/create-habit.html', {'habit_form': habit_form})
