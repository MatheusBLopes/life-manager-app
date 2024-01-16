from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .models import DayOfWeekChoice, Habit, HabitRecurrence, HabitSchedule, Week
from .utils.view_utils import calculate_weeks_and_years, create_schedules, format_date


@login_required
def habit_tracker(request, week_number=None, year=None):
    if week_number is None or year is None:
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_number = start_of_week.isocalendar()[1]
        year = today.year

    current_week, _ = Week.objects.get_or_create(week_number=week_number, year=year)

    week_days = current_week.day_set.all()

    for day in week_days:
        format_date(day)

        # Pega todas as recorrências que possivelmente possuem essa data
        active_recurrences = HabitRecurrence.objects.filter(
            Q(end_date__gte=day.date) | Q(end_date__isnull=True),
            start_date__lte=day.date,
        )

        if active_recurrences:
            # Loop through each active recurrence
            for recurrence in active_recurrences:
                # Determine the days of the week for which the habit should be scheduled
                days_to_schedule = recurrence.days_of_week.filter(day_of_week=day.date.strftime("%A"))

                # Check if there are days to schedule
                if days_to_schedule.exists():
                    HabitSchedule.objects.get_or_create(habit=recurrence.habit, day=day)

        day.habit_schedules = HabitSchedule.objects.filter(day=day).order_by("habit__name")

        for habit_schedule in day.habit_schedules:
            if habit_schedule.time_spent:
                habit_schedule.time_spent = int(round(habit_schedule.time_spent.total_seconds() / 60))

        # Count the number of successful habit schedules for the day
        successful_schedules_count = HabitSchedule.objects.filter(
            day=day, completion_status="success"
        ).count()

        # Calculate the percentage
        total_schedules_count = HabitSchedule.objects.filter(day=day).count()
        percentage_success = (
            (successful_schedules_count / total_schedules_count) * 100 if total_schedules_count > 0 else 0
        )

        day.percentage_success = round(percentage_success, 2)

    previous_year, next_year, previous_week, next_week = calculate_weeks_and_years(
        current_week.week_number, current_week.year
    )

    return render(
        request,
        "habit_tracker/pages/week.html",
        context={
            "days": week_days,
            "week": {
                "previous_week": previous_week,
                "next_week": next_week,
                "current_week": current_week.week_number,
                "present_week": datetime.now().date().isocalendar()[1],
            },
            "previous_year": previous_year,
            "next_year": next_year,
            "current_year": year,
            "present_year": datetime.now().date().year,
        },
    )


@login_required
def create_habit(request):
    if request.method == "POST":
        # Accessing the selected habit ID
        habit_name = request.POST.get("habit_name", None)

        habit = Habit.objects.create(name=habit_name, user=request.user)

        form_days_of_week = request.POST.getlist("day_of_week")
        db_days_of_week = DayOfWeekChoice.objects.filter(day_of_week__in=form_days_of_week)

        start_date = request.POST.get("start_date", None)
        end_date = request.POST.get("end_date", None)

        if not end_date:
            end_date = None

        habit_recurrence = HabitRecurrence.objects.create(
            habit=habit, start_date=start_date, end_date=end_date
        )
        habit_recurrence.days_of_week.add(*db_days_of_week)
        habit_recurrence.save()

        create_schedules(habit, habit_recurrence, db_days_of_week)

        return HttpResponseRedirect(reverse("habit_tracker:habit_tracker"))
    else:
        habits = Habit.objects.all()

    return render(request, "habit_tracker/pages/create-habit.html", context={"habits": habits})


@login_required
def update_recurrence(request):
    if request.method == "POST":
        form_days_of_week = request.POST.getlist("day_of_week")
        start_date = request.POST.get("start_date", None)
        habit_to_update_id = request.POST.get("habit_to_update", None)

        if not all([form_days_of_week, start_date, habit_to_update_id]):
            return HttpResponseBadRequest("Invalid form data.")

        try:
            habit_to_update = Habit.objects.get(id=habit_to_update_id)
        except Habit.DoesNotExist:
            return HttpResponseBadRequest("Invalid habit id.")

        # Parse start_date to a datetime object
        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()

        recurrence = HabitRecurrence.objects.filter(
            habit=habit_to_update,
        ).first()

        # Update days_of_week for the recurrence
        recurrence.days_of_week.set(DayOfWeekChoice.objects.filter(day_of_week__in=form_days_of_week))
        recurrence.start_date = start_date
        recurrence.save()

        # Delete schedules after the start_date
        schedules_to_delete = HabitSchedule.objects.filter(
            habit=habit_to_update,
            day__date__gte=start_date,
        )

        schedules_to_delete.delete()

        return redirect("habit_tracker:habit_tracker")

    else:
        habits = Habit.objects.all()
        return render(request, "habit_tracker/pages/update-recurrence.html", context={"habits": habits})


class MarkCompletedView(View):
    def post(self, request, *args, **kwargs):
        habit_schedule_id = request.POST.get("habit_schedule_id")

        habit_schedule = HabitSchedule.objects.get(id=habit_schedule_id)

        if habit_schedule:
            completion_status = request.POST.get("completion_status", None)
            description = request.POST.get("description", None)
            time_spent = request.POST.get("time_spent", None)

            habit_schedule.completion_status = completion_status
            habit_schedule.description = description

            # Convert time_spent to timedelta and update the habit_schedule
            if time_spent is not None:
                time_spent_minutes = int(time_spent)
                habit_schedule.time_spent = timedelta(minutes=time_spent_minutes)

            habit_schedule.save()

        return redirect("habit_tracker:habit_tracker", week_number=kwargs["week"], year=kwargs["year"])
