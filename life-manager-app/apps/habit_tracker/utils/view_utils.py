from datetime import datetime, timedelta

from apps.habit_tracker.models import Day, HabitSchedule, Week


def calculate_weeks_and_years(week_number, year):
    if 1 <= week_number <= 52:
        next_week = (week_number % 52) + 1
        previous_week = (week_number - 2) % 52 + 1
        previous_year = year - 1 if week_number == 1 else year
        next_year = year + 1 if week_number == 52 else year
    else:
        raise ValueError("Invalid week number. It should be between 1 and 52.")
    return previous_year, next_year, previous_week, next_week


# Helper function for formatting dates
def format_date(day):
    day.day_name = day.date.strftime("%A")
    day.formated_date = day.date.strftime("%d/%m/%Y")


def create_schedules(habit, habit_recurrence, db_days_of_week):
    start_date = datetime.strptime(habit_recurrence.start_date, "%Y-%m-%d")
    final_date = start_date + timedelta(days=7)
    selected_dates = []
    db_days_list = db_days_of_week.values_list("day_of_week", flat=True)
    current_date = start_date

    # Loop through dates until reaching the end date
    while current_date <= final_date:
        # Check if the current date's day of the week is in the selected days
        if current_date.strftime("%A") in db_days_list:
            selected_dates.append(current_date)

        # Move to the next day
        current_date += timedelta(days=1)

    for date in selected_dates:
        Week.objects.get_or_create(week_number=date.isocalendar()[1], year=date.year)

    days_to_schedule = Day.objects.filter(date__in=selected_dates)

    for day in days_to_schedule:
        HabitSchedule.objects.create(habit=habit, day=day)
