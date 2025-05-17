from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('add_car/', views.add_car, name='add_car'),
    path('car_detail/<int:id>/', views.car_detail, name='car_detail'),
]
