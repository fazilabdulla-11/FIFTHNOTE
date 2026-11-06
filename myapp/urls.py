from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),

    path('perfume/<int:pk>/', views.perfume_detail, name='detail'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('cart/add/<int:pk>/<str:size>/', views.add_to_cart, name='add_to_cart'),

    path('cart/increase/<int:pk>/<str:size>/', views.increase_cart, name='increase_cart'),

    path('cart/decrease/<int:pk>/<str:size>/', views.decrease_cart, name='decrease_cart'),

    path('cart/remove/<int:pk>/<str:size>/', views.remove_from_cart, name='remove_from_cart'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('my_orders/', views.my_orders, name='my_orders'),
    path('my_orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
]