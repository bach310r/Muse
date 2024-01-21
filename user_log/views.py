from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic




# Create your views here.


# class Login_View(generic.DetailView):
#     template_name = "user_log/detail.html"


# class Sign_Up_View(generic.DetailView):
#     template_name = "user_log/results.html"

def login(request):
    return render(request, "user_log/login.html")

def signup(request):
    return render(request, "user_log/signup.html")