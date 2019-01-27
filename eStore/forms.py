from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from eStore.models import Profile, Contact_us
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


        
class profileForm(forms.ModelForm):
	address_1 = forms.CharField(
		widget=forms.TextInput(
			attrs={'placeholder': 'Enter street address'}
		),
		max_length=600,
		required=False)

	address_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter street address'}
        ),
        max_length=600,
        required=False)


	phone_number= forms.CharField( widget=forms.TextInput(
		attrs={'placeholder': 'Enter your 10 digit mobile number without prefix +91, or 0.'}
		),
		required=False,
		validators=[validate_india_mobile_no]
	)
    
	class Meta:
		model = Profile
		fields = '__all__'
        
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
        
	

