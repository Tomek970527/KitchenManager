from django.forms import fields_for_model
from django.shortcuts import render
from .models import Profile, FoodProduct, FoodGroup, FoodPrice, NutritionalValue
from django.contrib.auth.models import User
import datetime
# Create your views here.

def register(request):
    context = {}
    return render(request, 'base/register.html')

def login(request):
    context = {}
    return render(request, 'base/login.html')

def password(request):
    context = {}
    return render(request, 'base/password.html')

def food_analysis_dashboard(request):
    food = FoodProduct.objects.all()
    context = {"food": food}
    return render(request, 'base/food_analysis.html', context)

def cost_analysis_dashboard(request):
    prices = FoodPrice.objects.all()
    context = {"prices": prices}
    return render(request, 'base/cost_analysis.html', context)

def profile(request):
    context = {}
    return render(request, 'base/profile.html', context)

def add_food_product(request):
    context = {}
    return render(request, 'base/food_product_form.html', context)

def edit_food_product(request):
    context = {}
    return render(request, 'base/food_product_form.html', context)

def delete_food_product(request):
    context = {}
    return render(request, 'base/food_product_form.html', context)

def add_profile(request):
    context = {}
    return render(request, 'base/profile_form.html', context)

def edit_profile(request):
    context = {}
    return render(request, 'base/profile_form.html', context)

def delete_profile(request):
    context = {}
    return render(request, 'base/profile_form.html', context)