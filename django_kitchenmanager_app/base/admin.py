from django.contrib import admin
from .models import FoodCategory, Kitchen, FoodProduct, FoodCost, FoodControl
# Register your models here.
admin.site.register(FoodCategory)
admin.site.register(Kitchen)
admin.site.register(FoodProduct)
admin.site.register(FoodCost)
admin.site.register(FoodControl)