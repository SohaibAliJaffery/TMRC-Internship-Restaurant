from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Lower # for case-insensitive ordering
# This file contains the models for the base application.

# Restaurant model
# User model
# Rating model

class Restaurant(models.Model):
  class TypeChoices(models.TextChoices):
    INDIAN = 'IN', 'Indian'
    ITALIAN = 'IT', 'Italian'
    CHINESE = 'CH', 'Chinese'
    MEXICAN = 'MX', 'Mexican'
    AMERICAN = 'AM', 'American'
    JAPANESE = 'JP', 'Japanese'
    FRENCH = 'FR', 'French'
    THAI = 'TH', 'Thai'
    GREEK = 'GR', 'Greek'
    FAST_FOOD = 'FF', 'Fast Food'
    OTHER = 'OT', 'Other'
  

  name = models.CharField(max_length=100)
  website = models.URLField(default='')
  date_opened = models.DateField()
  latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
  longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
  restaurant_type = models.CharField(
      max_length=2,
      choices=TypeChoices.choices,
      default=TypeChoices.OTHER
  )
  capacity = models.PositiveSmallIntegerField(null=True, blank=True)

  class Meta:
    ordering = [Lower('name')]  # Default ordering by name, case-insensitive
    get_latest_by = 'date_opened'  # Allows using .latest() method

  def __str__(self):
    return self.name
  


class Rating(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ratings')
  rating = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)]
  )

  def __str__(self):
    return f"{self.rating}/5"
  


class Sale(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name='sales')
  income = models.DecimalField(max_digits=10, decimal_places=2)
  datetime = models.DateTimeField()

  # def __str__(self):
  #   return f"Sale at {self.restaurant.name} on {self.datetime.strftime('%Y-%m-%d %H:%M:%S')} - ${self.income:.2f}"


class Staff(models.Model):
  name = models.CharField(max_length=128)
  restaurants = models.ManyToManyField(Restaurant, through='StaffRestaurant')
  # generates junction table automatically
  def __str__(self):
    return f"{self.name}"


class StaffRestaurant(models.Model):
  staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  salary = models.FloatField(null=True)
  

class Spending(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='spendings')
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  category = models.CharField(max_length=64)  # e.g., 'Rent', 'Utilities', 'Supplies', etc.
  description = models.TextField(blank=True)
  date = models.DateField()

  def __str__(self):
    return f"{self.restaurant.name} - {self.category}: {self.amount}"


class Product(models.Model):
  name = models.CharField(max_length=100)
  number_in_stock = models.PositiveSmallIntegerField()

  def __str__(self):
    return self.name
  

class Order(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
  number_of_items = models.PositiveSmallIntegerField()
  # user

  def __str__(self):
    return f'{self.number_of_items} x {self.product.name}'
