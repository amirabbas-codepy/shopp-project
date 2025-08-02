
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app_shop_api.views import *
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reg/', register, name='register'),
    path('home/', send_all_products, name='home'),
    path('serch/', serch_products, name='serch'),
    path('selectp/', select_product, name='select'),
    path('psc/', proccess_shopping_cart, name='psc'),
    path('del/', delete_user, name='del'),
    path('delete_product_in_cart/', delete_seleceted_products_in_shopping_card, name='delpr'),
    path('showcart/', show_shopping_cart, name='ssc'),
    path('comment/', comment, name='comment'),
    path('showcomments/', show_comments, name='showcomments'),
    path('final/', final_shopping_cart_registarion, name='final'),
    path('sfr/', show_final_registarions, name='sfr'),
    path('details/<int:idp>', details_product, name='details'),
]