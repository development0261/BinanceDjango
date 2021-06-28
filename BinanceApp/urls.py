
from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path("",index,name="index"),
    path("get_coin_price/",get_coin_price,name="get_coin_price")
]