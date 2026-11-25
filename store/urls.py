
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.my_profile, name='profile'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),

    path('decrease-quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.my_wishlist, name='wishlist'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('checkout/', views.checkout, name='checkout'),
    path(
    'place-order/',
    views.place_order,
    name='place_order'),
    path(
    'order-confirmation/<int:order_id>/',
    views.order_confirmation,
    name='order_confirmation'),
    
    path(
    'track-order/<int:order_id>/',
    views.track_order,
    name='track_order'),
    
    path(
    'cancel-order/<int:order_id>/',
    views.cancel_order,
    name='cancel_order'),


]
