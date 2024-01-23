from django.urls import path

from . import views

app_name = 'user_log'
urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),

]
