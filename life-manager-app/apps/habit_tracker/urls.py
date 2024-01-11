from django.urls import path

from . import views

app_name = "habit_tracker"
urlpatterns = [
    path("habit-tracker/", views.habit_tracker, name="habit_tracker"),
    path("habit-tracker/<int:week_number>/<int:year>", views.habit_tracker, name="habit_tracker"),
    path("habit-tracker/create-habit/", views.create_habit, name="create_habit"),
    path("habit-tracker/update-recurrence/", views.update_recurrence, name="update_recurrence"),
    path(
        "mark-completed/<int:week>/<int:year>/<str:date>/",
        views.MarkCompletedView.as_view(),
        name="mark_completed",
    ),
]
