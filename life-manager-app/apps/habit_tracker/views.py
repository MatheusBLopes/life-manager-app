from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Habit, HabitCompletion
from .forms import HabitForm, HabitCompletionForm
from django.db.models import Q
from django.views import View

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

        habits_with_desired_day = Habit.objects.filter(
            Q(days_of_week__name=day_name[0:3]) &
            Q(user=user) &
            (Q(start_date__lte=current_date) & 
            (Q(end_date__gte=current_date) | Q(end_date__isnull=True))
        ))

        completed_habits_count = 0
        total_habits_count = len(habits_with_desired_day)

        for habit in habits_with_desired_day:
            habit_completion = HabitCompletion.objects.filter(habit=habit, creation_date=current_date).first()
            
            if not habit_completion:
                HabitCompletion.objects.create(habit=habit, creation_date=current_date, completion_status="not_completed")
                habit_completion = HabitCompletion.objects.filter(habit=habit, creation_date=current_date).first()


            habit.completion_status = habit_completion.completion_status

            if habit.completion_status == 'success':
                completed_habits_count += 1

            initial_data = {
                "habit": habit.id,
                "date_completed": current_date,
                "completion_status": habit.completion_status,
                "description": habit_completion.description,
                "time_spent": habit_completion.time_spent
            }
            
            habit.completion_form = HabitCompletionForm(initial=initial_data)

        percentage_completed = round((completed_habits_count / total_habits_count) * 100, 2) if total_habits_count > 0 else 0

        days.append({
            "date": current_date.strftime("%d/%m/%Y"),
            "raw_date": current_date.strftime("%Y-%m-%d"),
            "day_name": day_name,
            "habits": habits_with_desired_day,
            "percentage_completed": percentage_completed
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
        year = today.year
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
                'next_week': next_week,
                'current_week': week_number,
                'present_week': datetime.now().date().isocalendar()[1]
            },
            "previous_year": previous_year,
            "next_year": next_year,
            "current_year": year,
            "present_year": datetime.now().date().year,
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


class MarkCompletedView(View):

    def post(self, request, *args, **kwargs):
        breakpoint()
        habit_id = request.POST.get('habit_id')
        habit = Habit.objects.get(id=habit_id, user=request.user)

        date_completed = kwargs['date']
        success = request.POST.get('success', 'false').lower() == 'true'  # Default to False if not provided or not 'true'

        # Check if the habit completion record exists for the selected day
        habit_completion = habit.habitcompletion_set.filter(date_completed=date_completed).first()

        if habit_completion:
            # If habit completion exists, update the success field
            habit_completion.success = success
            habit_completion.save()
        else:
            # If habit completion doesn't exist, create a new record with the provided success value
            HabitCompletion.objects.create(habit=habit, date_completed=date_completed, success=success)

        return redirect('habit_tracker:habit_tracker', week_number=kwargs['week'], year=kwargs['year'])