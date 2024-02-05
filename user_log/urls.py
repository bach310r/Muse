from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from . import views

app_name = 'user_log'
urlpatterns = [
    path("", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name='logout'),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path('update-email/', views.update_email, name='update_email'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
