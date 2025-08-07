from django.contrib import admin
from app_shop.views import *
from django.urls import path
urlpatterns = [
    path('registertemp/', register, name='registertemp'),
    path('hometemp/', home_view, name='hometemp'),
    path('logintemp/', login_view, name='logintemp'),
    path('logouttemp/', logout_view, name='logouttemp'),
    path('detailstemp/<int:idp>/', details, name='detailstemp'),
    path('selectproducttemp/<int:idp2>/', seletc_product_view, name='selectproducttemp'),
    path('profiletemp/', profile, name='profiletemp'),
    path('commenttemp/<int:idp3>/', comment_view, name='commenttemp'),
    path('showcommenttemp/<int:idp4>/', show_comments, name='showcommenttemp'),
    path('deleteselectedtemp/<int:idp5>/', delete_selected_product, name='deleteselectedtemp'),
    path('serchtemp/', serch_product, name='serchtemp'),
    path('shoppingcarttemp/', shopping_cart, name='shoppingcarttemp'),
    path('finalregistertemp/', final_shopping_cart_registarion, name='finalregistertemp'),
    path('editadrtemp/', edit_adress, name='editadrtemp'),
    path('deltemp/', deleted_account, name='deltemp'),

]
