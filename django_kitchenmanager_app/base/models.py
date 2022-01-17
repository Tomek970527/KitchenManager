from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Kitchen(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class FoodCategory(models.Model):
    name = models.CharField(max_length=120, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class FoodProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False, blank=False)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True)
    macro = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class FoodControl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_product = models.OneToOneField(FoodProduct, on_delete=models.CASCADE, null=False)
    expiration_date = models.DateField(null=False, blank=False)
    opening_date = models.DateField(null=True)
    require_refrigeration_before_opening = models.BooleanField()
    require_refrigeration_after_opening = models.BooleanField()
    time_to_consume = models.DurationField()

    def __str__(self):
        return self.expiration_date

class FoodCost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=120)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.food_name}: {str(self.price_paid)} PLN'