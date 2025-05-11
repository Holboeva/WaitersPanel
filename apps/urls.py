from django.urls import path
from . import views

urlpatterns = [
    path('tables/', views.tables_view, name='tables'),
    path('menu/<int:table_id>/', views.menu_view, name='menu'),
    path('menu/<int:table_id>/add/<int:menu_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:table_id>/', views.view_cart, name='view_cart'),
    path('cart/<int:table_id>/remove/<str:item_key>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/<int:table_id>/place/', views.place_order, name='place_order'),
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
]
