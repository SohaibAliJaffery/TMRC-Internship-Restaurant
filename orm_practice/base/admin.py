from django.contrib import admin
from .models import Restaurant, Rating, Sale, Staff, StaffRestaurant, Spending, Product, Order

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Rating)
admin.site.register(Sale)
admin.site.register(Staff)
admin.site.register(Spending)
admin.site.register(StaffRestaurant)
admin.site.register(Order)
admin.site.register(Product)



