
from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path("",index,name="index"),
    path("get_coin_price/",get_coin_price,name="get_coin_price"),
    path("get_coins/",get_coins,name="get_coins"),
    path("load_more/<int:num_posts>/",load_more,name="load_more"),
    path("load_more_view/",load_more_view,name="load_more_view"),
]