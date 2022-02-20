from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_analysis_dashboard, name="food-analysis-dashboard"),
    path('website/', views.index, name="index")
    # path('/costs', views)
]