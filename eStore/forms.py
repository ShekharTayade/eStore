from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from eStore.models import ORder, Order_Details

from django.core.validators import validate_slug, MinLengthValidator

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.utils.translation import gettext_lazy as _

from string import Template
from django.forms import ImageField


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 
                 'password2')

        
class ProfileForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':2, 'placeholder': 'Enter address'}
        ),
        max_length=2000,
        help_text='The max length is 3000 characters.',
        required=False)

    education = forms.CharField( widget=forms.TextInput(
        attrs={'placeholder': 'Please enter the currently pursuing (ex. X, XI, XII, B.E. etc.)'}
        ),
        required=False
    )

    phone_number= forms.CharField( widget=forms.TextInput(
        attrs={'placeholder': 'Enter your 10 digit mobile number without prefix +91, or 0.'}
        ),
        required=False,
        validators=[validate_india_mobile_no]
    )
    
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'gender', 'address', 'city', 'state', 'phone_number', 'education')
        


class OrderShippingForm(forms.ModelForm):
    percentage_weight = forms.FileField(label="Alloc")
    class Meta:
        model = Oder_shipping
        fields = ('order_shipping_id', 'store', 'order_id', 'user',
		'shipping_address','full_name', 'company', 'address_1','address_2',
		'city_id', 'state_id', 'pin_code', 'country_id', 'phone_number',
		'email_id', 'updated_date')
