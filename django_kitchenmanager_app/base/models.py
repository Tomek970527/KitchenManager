from locale import currency
from tkinter import CHORD
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import uuid

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    # profile_image = models.ImageField(upload_to='images/')
    facebook_link = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class FoodGroup(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class FoodProduct(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(FoodGroup, on_delete=models.SET_NULL, null=True, blank=True)
    needs_cooling = models.BooleanField()
    expiration_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class NutritionalValue(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    food_name = models.CharField(max_length=200)
    food_product = models.ForeignKey(FoodProduct, on_delete=models.SET_NULL, null=True, blank=True)
    fat = models.FloatField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    calories = models.FloatField()

    def __str__(self):
        return self.food_name

class FoodPrice(models.Model):
    CURRENCY_TYPE = (
        ('EUR', 'euro'),
        ('PLN', 'polish złoty'),
        ('USD', 'dollar'),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    value = models.FloatField()
    currency = models.CharField(max_length=200, choices=CURRENCY_TYPE)
    food_name = models.CharField(max_length=200)
    shop_name = models.CharField(max_length=200)
    food_product = models.ForeignKey(FoodProduct, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food_name + ' | ' + str(self.value) + ' | ' + self.currency + ' | ' + str(self.created.strftime("%d.%m.%Y")) 





