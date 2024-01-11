from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "finance"


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("purchases/", views.PurchaseListView.as_view(), name="purchases"),
]
