from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("apps.finance.urls", namespace="finance")),
    path('', include("apps.habit_tracker.urls", namespace="habit_tracker")),
]
