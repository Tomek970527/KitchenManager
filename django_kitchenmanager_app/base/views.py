from django.shortcuts import render
from .models import Profile, FoodProduct, FoodGroup, FoodPrice, NutritionalValue
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    food = FoodProduct.objects.all()
    prices = FoodPrice.objects.all()
    context = {"food": food, "prices": prices}
    return render(request, 'base/home.html', context)
