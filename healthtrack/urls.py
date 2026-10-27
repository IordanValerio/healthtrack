from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("bmi/", views.bmi, name="bmi"),
    path("nutrition/", views.nutricao, name="nutrition"),
    path("exercises/", views.exercises, name="exercises"),
]