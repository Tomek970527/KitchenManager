from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_analysis_dashboard, name="food-dashboard"),
    path('cost/', views.cost_analysis_dashboard, name="cost-dashboard"),
    path('login/', views.login, name="login"),
    path('password/', views.password, name="forgot-password"),
    path('register/', views.register, name="register")
    # path('/costs', views)
]