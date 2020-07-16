from django import forms
from .models import Address
from django.forms import (
    ModelForm, 
    Textarea, 
    TextInput,
    Select
) 

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'country',
            'state',
            'city',
            'postal_code',
            'address_line1',
            'address_line2'
        ]
        
        # Form attribute
        # billing_profile = Select(attrs={
        #     'class': 'form-control',
        #     'type': 'hidden',
        # })
        country = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Country',
        })
        state = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your State',
        })
        city = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your City',
        })
        postal_code = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Postal Code',
        })
        address_line1 = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address line 1',
        })
        address_line2 = TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address line 2... optional',
        })

        widgets = {
            # 'billing_profile': billing_profile,
            'country': country,
            'state': state,
            'city': city,
            'postal_code': postal_code,
            'address_line1': address_line1,
            'address_line2': address_line2,
        }