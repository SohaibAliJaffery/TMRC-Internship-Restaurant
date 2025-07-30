from django import forms
# from .models import Restaurant, Rating, Sale
from django.core.validators import MinValueValidator, MaxValueValidator

class RatingForm(forms.Form):
  rating = forms.IntegerField(
    label='Rating',
    validators=[MinValueValidator(1), MaxValueValidator(5)]
  )