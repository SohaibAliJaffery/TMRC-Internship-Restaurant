from django.shortcuts import render
from .forms import RatingForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Restaurant, Rating, Sale, Staff, StaffRestaurant, Spending, Product, Order
from .serializers import RestaurantSerializer, RatingSerializer, SaleSerializer, RestaurantSummarySerializer, RatingDetailSerializer, FiveStarRestaurantSalesSerializer, GetStaffForAllRestaurantsSerializer, ProductOrderSerializer
from django.shortcuts import get_object_or_404
from django.db.models import StdDev, Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from django.db import transaction


# Create your views here.
def index(request):
  restaurants = Restaurant.objects.all()
  context = {
    'restaurants': restaurants,
  }

  return render(request, 'index.html', context)


@api_view(['GET'])
def restaurant_list(request):
  # restaurants = Restaurant.objects.all()
  restaurants = Restaurant.objects.prefetch_related('ratings') # Prefetch related ratings to optimize query
  # If no restaurants exist, return a message
  if not restaurants:
    return Response({"status":"failed", "message": "No records found."}, status=404)  # Return a message if no items exist
  serializer = RestaurantSummarySerializer(restaurants, many=True)
  return Response({"status":"success", "data": serializer.data})  # Return a success status with serialized data

@api_view(['GET'])
def restaurant_detail(request):
  # pk= request.query_params.get('pk')
  pk = request.GET.get('id')
  if not pk:
    return Response({"status":"failed",  "message": "Restaurant ID is required"}, status=400)  # Return a message if ID is not provided
  restaurant = get_object_or_404(Restaurant, pk=pk)
  if not restaurant:
    return Response({"status":"failed", "message": "Item not found"}, status=404)  # Return a message if item does not exist
  serializer = RestaurantSerializer(restaurant)
  return Response({"status":"success", "data": serializer.data})


@api_view(['GET'])
def rating_list_for_restaurant(request, restaurant_id):
  ratings = Rating.objects.filter(restaurant_id=restaurant_id)
  if not ratings:
    return Response({"status":"failed", "message": "No ratings found for this restaurant"}, status=404)  # Return a message if no ratings exist
  serializer = RatingSerializer(ratings, many=True)
  return Response({"status":"success", "data":serializer.data})


@api_view(['GET'])
def get_all_ratings(request):
  ratings = Rating.objects.only('rating', 'restaurant__name').select_related('restaurant')  # Use select_related to optimize query and only fetch necessary fields
  if not ratings:
    return Response({"status":"failed", "message": "No ratings found"}, status=404)  # Return a message if no ratings exist
  serializer = RatingDetailSerializer(ratings, many=True)
  return Response({"status":"success", "data":serializer.data})


# get all 5 star rating restaurants and fetch all sales for those restaurants
@api_view(['GET'])
def five_star_restaurants_sales(request):
  five_star_restaurants = Restaurant.objects.prefetch_related('ratings', 'sales').filter(ratings__rating=5).distinct()
  if not five_star_restaurants:
    return Response({"status":"failed", "message": "No 5-star restaurants found"}, status=404)  # Return a message if no 5-star restaurants exist
  serializer = FiveStarRestaurantSalesSerializer(five_star_restaurants, many=True)
  return Response({"status":"success", "data":serializer.data})
  

@api_view(['GET'])
def get_staff_for_all_restaurants(request):
  jobs = StaffRestaurant.objects.prefetch_related('restaurant', 'staff')
  if not jobs:
    return Response({"status":"failed", "message": "No staff found for any restaurant"}, status=404)  # Return a message if no staff exist
  serializer = GetStaffForAllRestaurantsSerializer(jobs, many=True)
  return Response({"status":"success", "data": serializer.data})


@api_view(['POST'])
def add_sale(request):
  serializer = SaleSerializer(data = request.data)
  if serializer.is_valid():
    serializer.save()
  return Response({"status":"success", "data":serializer.data},status=201)


# @api_view(['POST'])
# def add_spending()

@api_view(['GET'])
def get_net_income_1(request):
  pk = request.GET.get('id')
  if not pk:
    return Response({"status": "failed", "message": "Restaurant ID is required"}, status=400)

  restaurant = get_object_or_404(Restaurant, pk=pk)
    
  sales_total = restaurant.sales.aggregate(total=Sum('income'))['total'] or 0
  spendings_total = restaurant.spendings.aggregate(total=Sum('amount'))['total'] or 0
  net_income = round(sales_total - spendings_total, 2)

  return Response({
    "status": "success",
    "data": {
      "name": restaurant.name,
      "net_income": net_income
    }
  })


from .serializers import RestaurantNetIncomeSerializer

@api_view(['GET'])
def get_net_income_2(request):
  pk = request.GET.get('id')
  if not pk:
    return Response({"status": "failed", "message": "Restaurant ID is required"}, status=400)

  restaurant = get_object_or_404(Restaurant.objects.prefetch_related('sales', 'spendings'), pk=pk)
  serializer = RestaurantNetIncomeSerializer(restaurant)
  return Response({"status": "success", "data": serializer.data})

from .serializers import AllRestaurantNetIncomeSerializer
@api_view(['GET'])
def get_net_income_for_all(request):
  restaurants = Restaurant.objects.annotate(
    total_sales=Sum('sales__income'),
    total_spendings=Sum('spendings__amount'),
    net_income=F('total_sales') - F('total_spendings')
  )
  serializer = AllRestaurantNetIncomeSerializer(restaurants, many=True)
  return Response({"status": "success", "data": serializer.data})

@api_view(['POST'])
def order_product(request):
  serializer = ProductOrderSerializer(data=request.data)
  if serializer.is_valid():
    with transaction.atomic():
      product = Product.objects.get(pk=serializer.validated_data['product'].id)
      num_items = serializer.validated_data['number_of_items']
      if product.number_in_stock < num_items:
        return Response({"status": "failed", "message": "Not enough stock"}, status=400)
      order = serializer.save()
      product.number_in_stock -= num_items
      product.save()
      return Response({"status": "success", "data": serializer.data}, status=201)
  return Response({"status": "failed", "message": "Invalid data"}, status=400)