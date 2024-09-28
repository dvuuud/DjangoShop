from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<slug:slug>/', views.cart_add, name='cart_add'),
    path('cart/remove/<slug:slug>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),

]
