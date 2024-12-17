from django.urls import path
from .views import *

urlpatterns = [
    path('',homepage,name="home" ),
    path('register/',registerpage,name="register"),
    path('cart/',cart_page,name="cart"),
    path('fav/',fav_page,name="fav"),
    path('favview/',fav_view,name="favview"),
    path('remove_cart/<str:cid>',remove_cart,name="remove_cart"),
    path('remove_fav/<str:fid>',remove_fav,name="remove_fav"),
    path('login/',loginpage,name="login"),
    path('logout/',logoutpage,name="logout"),
    path('collection/',collectionpage,name="collect"),
    path('collections/<str:name>',collectionpageview,name="collect"),
    path('collections/<str:cname>/<str:pname>',product_details,name="product_details"),
    path('addtocart/',add_to_Cart,name='addtocart')

]