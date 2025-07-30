from django.contrib.auth.models import User
from base.models import Restaurant, Rating, Sale, Staff, StaffRestaurant, Spending
from django.db.models.functions import Upper
from django.utils import timezone
from django.db import connection
from datetime import date, timedelta, datetime
from pprint import pprint
from django.db.models.functions import Lower # for case-insensitive ordering
import random
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, Value, CharField
import itertools

# Inspect SQL: python manage.py shell_plus --print-sql 
def run():











#   # aggregate total sales for each restaurant
#   # 1 - 10th
#   # 10 -  11th etc

#   first_sale = Sale.objects.aggregate(first_sale_date=Min('datetime'))['first_sale_date']
#   last_sale = Sale.objects.aggregate(last_sale_date=Max('datetime'))['last_sale_date']

#   # generate a list of dates 10 days apart:
#   dates= []
#   count = itertools.count()

#   while (dt:= first_sale + timedelta(days=10*next(count))) <= last_sale:
#     dates.append(dt)

#   whens = [
#     When(datetime__range=(dt, dt + timedelta(days=10)), then=Value(dt.date()))
#     for dt in dates
#   ]
#   case = Case(
#     *whens,
#     output_field = CharField()
#   ) 

#   print(Sale.objects.annotate(
#     daterange=case
#   ).values('daterange').annotate(total_sales = Sum('income')))
# #         .values('name', 'nsales'))
# #   pprint(connection.queries)

