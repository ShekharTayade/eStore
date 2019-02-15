from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, DatabaseError, Error

from django.urls import resolve
from django.contrib import messages
   
from .cart_views import *
from eStore.forms import registerForm, businessprofile_Form, businessuserForm
   
def eStorelogin(request):

	if request.method == 'POST':
    
		# Get current session details
		sessionid = request.session.session_key
	
		
		username = request.POST['username'] 
		password = request.POST['password']
		email = request.POST['email']
		next = request.POST['curr_pg']
		
		user = authenticate(request, email=email, username=username, password=password)
	   
		if user is not None :
            
			login(request, user)
			
			if not request.POST.get('remember', None):
				request.session.set_expiry(0)   
	
			# Let's sync the cart for the session and logged in user
			sync_cart_session_user(request, sessionid)
	
			return redirect(next)
        
		else :

			messages.add_message(request, messages.ERROR, 'Your credentials did not match. Please try again.')		
			return redirect(next)
			#return render(request, 'eStore/estore_base.html', {
			#	'username' : request.user.username, 'auth_user' : 'FALSE'})
	else:
		
		messages.add_message(request, messages.ERROR, 'Unauthozied login tried.')		
		return render(request, 'eStore/estore_base.html')

	
def register(request):

	if request.method == 'POST':
		next = request.POST['curr_pg']
		form = registerForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

			# After successful sign up redirect to cuurent page
			return redirect('index')
	else:
		form = registerForm()
	return render(request, "eStore/register.html", {'form':form} )
	
	
def business_registration(request):

    
    if request.method == 'POST':
        form = businessuserForm(request.POST)
        businessprofile_form = businessprofile_Form(request.POST)
        if form.is_valid():
            if businessprofile_Form.is_valid():

                user = form.save()
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                userprofile = businessprofile_form.save(commit=False)
                userprofile.User = user
                userprofile_form.save()
            
                # After successful sign up redirect to payment page
                return redirect('index')
    else:
        form = businessuserForm()
        businessprofile_form = businessprofile_Form()        
    return render(request, 'eStore/business_registration.html', {'form': form, 'businessprofile_form': businessprofile_form})
