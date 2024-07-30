from django import forms
from .models import *


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['realtor', 'title', 'address', 'city', 'state',
                  'zipcode', 'description', 'price', 'bedrooms',
                  'bathrooms', 'garage', 'sqft', 'lot_size', 'photo_main',
                  'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6',
                  'is_published']

class RealtorForm(forms.ModelForm):
    class Meta:
        model = Realtor
        fields = ['name', 'photo', 'description', 'phone', 'email', 'is_mvp', 'hire_date']