from rest_framework import serializers
from .models import Restaurant, Rating, Sale, Staff, StaffRestaurant, Order, Spending, Product

class RestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Restaurant
    fields = '__all__'
    #read_only_fields = ('created_at', 'updated_at')

class RatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rating
    fields = '__all__'
  

class SaleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sale
    fields = '__all__'


class RestaurantSummarySerializer(serializers.ModelSerializer):
  average_rating = serializers.SerializerMethodField()
  restaurant_type = serializers.CharField(source='get_restaurant_type_display')

  class Meta:
    model = Restaurant
    fields = ['name', 'restaurant_type', 'average_rating']

  def get_average_rating(self, obj):
    ratings = obj.ratings.all()
    if ratings.exists():
        return round(sum(r.rating for r in ratings) / ratings.count(), 2)
    return None
  

class RatingDetailSerializer(serializers.ModelSerializer):
  restaurant_name = serializers.CharField(source='restaurant.name')
  class Meta:
    model = Rating
    fields = [ 'restaurant_name', 'rating' ]


class FiveStarRestaurantSalesSerializer(serializers.ModelSerializer):
  total_sales = serializers.SerializerMethodField()
  
  class Meta:
    model = Restaurant
    fields = ['name', 'total_sales']
  
  def get_total_sales(self, obj):
    sales = obj.sales.all()
    if sales.exists():
      return sum(sale.income for sale in sales)
    return 0.00
  

class GetStaffForAllRestaurantsSerializer(serializers.ModelSerializer):
  staff_name = serializers.CharField(source='staff.name')
  restaurant_name = serializers.CharField(source='restaurant.name')
  
  class Meta:
    model = StaffRestaurant
    fields = ['staff_name', 'restaurant_name', 'salary']
   

class RestaurantNetIncomeSerializer(serializers.ModelSerializer):
  net_income = serializers.SerializerMethodField()

  class Meta:
    model = Restaurant
    fields = ['name', 'net_income']

  def get_net_income(self, obj):
    total_sales = sum(sale.income for sale in obj.sales.all())
    total_spendings = sum(spending.amount for spending in obj.spendings.all())
    return round(total_sales - total_spendings, 2)


class AllRestaurantNetIncomeSerializer(serializers.ModelSerializer):
  total_sales = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
  total_spendings = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
  net_income = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

  class Meta:
    model = Restaurant
    fields = ['id', 'name', 'total_sales', 'total_spendings', 'net_income']

class ProductStockException(Exception):
  pass

class ProductOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = ('product', 'number_of_items')
