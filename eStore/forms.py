from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from eStore.models import Business_profile, Contact_us, User_image
from eStore.validators import validate_eStore_email, validate_contact_name
from eStore.validators import validate_image_size, validate_india_mobile_no
from django.core.validators import validate_slug, MinLengthValidator

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.utils.translation import gettext_lazy as _

from string import Template
from django.forms import ImageField


class registerForm(UserCreationForm):
	email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 
				 'password2')

class businessuserForm(UserCreationForm):
	email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
	class Meta:
		model = User
		fields = ('username','email', 'password1', 
				 'password2')

        
class businessprofile_Form(forms.ModelForm):
	current_address_1 = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'Suit / Floor / Building'}),
		required=False
	) 

	address_2 = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'Street / Locality'}),
		required=False
	) 

	pin_code = forms.CharField(
		widget=forms.TextInput(),
		required=False
	)	

	city = forms.CharField(
		widget=forms.TextInput(),
		required=False
	)	
	
	
	phone_number= forms.CharField( widget=forms.TextInput(
		attrs={'placeholder': 'Enter your 10 digit mobile number without prefix +91, or 0.'}
		),
		required=False,
		validators=[validate_india_mobile_no]
	)
    
	class Meta:
		model = Business_profile
		fields = ('contact_name', 'company', 'address_1', 'address_2',
			'city', 'state', 'pin_code', 'country', 'phone_number',
			'gst_number', 'tax_id')
			
        
class contactUsForm(forms.ModelForm):
	phone_number= forms.CharField( widget=forms.TextInput(
		attrs={'placeholder': 'Enter your 10 digit mobile number without prefix +91, or 0.'}
		),
		required=False,
		validators=[validate_india_mobile_no]
	)
    
	class Meta:
		model = Contact_us
		fields = '__all__'


        
class User_imageForm(forms.ModelForm):
	image_to_frame = forms.ImageField(
		validators=[validate_image_size],
		required=True
	)	
	class Meta:
		model = User_image
		fields = '__all__'

