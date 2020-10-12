from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User

from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 
            'biographie',
            'phone',
            'photo',
            'facebook',
            'whatsapp',
            'instagram'
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]
        
class ContactusForm(forms.ModelForm):
 
    class Meta:
        model = Contactus
        fields = '__all__'


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

# CITY_CHOICE = (
#     ('', ''),
#     ('', ''),
#     ('', ''),
#     ('', ''),
#     ('', ''),
#     ('', ''),
# )

class CheckoutForm(forms.Form):
    quartier_addresse = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control'
    }))
    apartment_addresse = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'entrer votre ville',
        'class': 'form-control'
    }))
    pays = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control',
        'data-placeholder': 'Choisissez votre pays'

    }))
    zip = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'entrer votre code postal',
        'class': 'form-control'
    }))
    # same_shipping_address = forms.BooleanField(required=False)
    # save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class BoutikForm(forms.ModelForm):
    class Meta:
        model = Boutique
        fields = [
            'name',
            'label', 
            'type_boutique', 
            'localite',
            'image', 
            'description'
        ]
    

class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemSeller
        fields = (
            'boutique',
            'title',
            'price',
            'discount_price',
            'label',
            'livraison',
            'size',
            'categories',
            'stock',
            'description_court',
            'description_long',
            'image',
            'photo_1',
            'photo_2',
            'photo_3',
            'photo_4',
            'is_active'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # restrict the queryset of 'Turma'
        self.fields['boutique'].queryset = self.fields['boutique'].queryset.filter(author=user)