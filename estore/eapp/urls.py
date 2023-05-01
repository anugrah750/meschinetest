from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('signup',views.signup),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('store',views.store,name="store"),
    path('cart',views.cart,name="cart"),
    path('update_item',views.updateItem,name="update_item"),
]