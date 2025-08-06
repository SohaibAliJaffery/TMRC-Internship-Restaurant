from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('restaurants/', views.restaurant_list, name='restaurant-list'),
  path('restaurant-detail/', views.restaurant_detail, name='restaurant-detail'),
  path('restaurants/<int:restaurant_id>/ratings/', views.rating_list_for_restaurant, name='restaurant-ratings'),
  path('ratings/', views.get_all_ratings, name='rating-list'),
  path('five-star-restaurants/sales/', views.five_star_restaurants_sales, name='five-star-restaurants-sales'),
  path('get-staff-for-all/', views.get_staff_for_all_restaurants, name='get-staff-for-all-restaurants'),
  path('get-net-income-1/', views.get_net_income_1, name='restaurant-net-income'),
  path('get-net-income-all/', views.get_net_income_for_all, name='all-restaurant-net-income'),
  path('order/', views.order_product, name='order-product'),
  path('order_locked/', views.order_product_locked_rows, name='order-product-locked'),

]






