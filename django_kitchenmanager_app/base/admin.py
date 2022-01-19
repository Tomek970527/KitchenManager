from queue import PriorityQueue
from django.contrib import admin
from .models import Profile, FoodProduct, FoodGroup, FoodPrice, NutritionalValue

# Register your models here.
admin.site.register(Profile)
admin.site.register(FoodProduct)
admin.site.register(FoodGroup)
admin.site.register(FoodPrice)
admin.site.register(NutritionalValue)

