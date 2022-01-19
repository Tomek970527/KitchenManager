# Generated by Django 3.2.11 on 2022-01-19 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_auto_20220119_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('needs_cooling', models.BooleanField()),
                ('expiration_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.foodgroup')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('facebook_link', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NutritionalValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('food_name', models.CharField(max_length=200)),
                ('fat', models.FloatField()),
                ('protein', models.FloatField()),
                ('carbohydrates', models.FloatField()),
                ('calories', models.FloatField()),
                ('food_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.foodproduct')),
            ],
        ),
        migrations.CreateModel(
            name='FoodPrice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('value', models.FloatField()),
                ('currency', models.CharField(choices=[('euro', 'EUR'), ('polish złoty', 'PLN'), ('dollar', 'USD')], max_length=200)),
                ('food_name', models.CharField(max_length=200)),
                ('shop_name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('food_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.foodproduct')),
            ],
        ),
    ]
