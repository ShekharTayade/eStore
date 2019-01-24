from django.urls import path
from django.conf.urls import url, include

from . import views

from django.contrib.auth import views as auth_views
from allauth.account.views import LoginView

urlpatterns = [
	url(r'^accounts/', include('allauth.urls')),
    url(r'^login/$', views.eStorelogin, name='login'),	
	url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),    
    url(r'^password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    
    url(r'^reset/$', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'), name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
       auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
       name='password_reset_confirm'),
    url(r'^reset/complete/$',
       auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
       name='password_reset_complete'), 
	
	path('', views.index, name='index'),

	
	
	
    url(r'^$', views.index, name='index'),	
    url(r'^register/$', views.register, name='register'),	
    url(r'^contact_us/$', views.contact_us, name='contact_us'),	
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^terms_conditions/$', views.terms_conditions, name='terms_conditions'),
    
	
	url(r'^faq/$', views.faq, name='faq'),

	path('product/<int:prod_id>/', views.product_details, name='product_details'),	
	path('category_prods/<int:cat_id>/', views.category_products, name='category_products'),	
    url(r'^all_products/$', views.all_products, name='all_products'),
	
	
    url(r'^basket/$', views.basket, name='basket'),
    url(r'^basket/$', views.show_frame, name='show_frame'),
	
	url(r'^ajax/add_to_cart/$', views.add_to_cart, name='add_to_cart'),
	url(r'^ajax/delete_cart_item/$', views.delete_cart_item, name='delete_cart_item'),
	url(r'^ajax/update_cart_item/$', views.update_cart_item, name='update_cart_item'),
	#path('update_cart_item/<int:qty>/', views.update_cart_item, name='update_cart_item'),	
	url(r'^ajax/show_mouldings/$', views.show_mouldings, name='show_mouldings'),
	url(r'^ajax/get_addr_pin_city_state/$', views.get_addr_pin_city_state, name='get_addr_pin_city_state'),
	url(r'^ajax/validate_address/$', views.validate_address, name='validate_address'),


 
    url(r'^show_cart/$', views.show_cart, name='show_cart'),
	url(r'^ajax/sync_cart_session_user/$', views.sync_cart_session_user, name='sync_cart_session_user'),


	
	path('show_collection/<int:coll_id>/', views.show_collection, name='show_collection'),	

    url(r'^import_image_data/$', views.importImageData, name='import_image_data'),
	
	path('show_frames/<int:frame_id>/', views.show_frames, name='show_frames'),	

	url(r'^show_all_categories/$', views.show_categories, name='show_all_categories'),
	
	url(r'^ajax/get_moulding_price/$', views.get_moulding_price, name='get_moulding_price'),
 	url(r'^ajax/get_mount_price/$', views.get_mount_price, name='get_mount_price'),
 	url(r'^ajax/get_board_price/$', views.get_board_price, name='get_board_price'),
 	url(r'^ajax/get_acrylic_price/$', views.get_acrylic_price, name='get_acrylic_price'),
 	url(r'^ajax/get_item_price/$', views.get_item_price, name='get_item_price'),
 	url(r'^ajax/get_FramedImage/$', views.get_FramedImage, name='get_framed_image'),
 	url(r'^ajax/apply_voucher/$', views.apply_voucher, name='apply_voucher'),

	url(r'^checkout_step1/$', views.checkout_step1_address, name='checkout_step1_address'),
	
	url(r'^checkout_step2/$', views.checkout_saveAddr_shippingMethod, name='checkout_saveAddr_shippingMethod'),
	url(r'^checkout_step3/$', views.checkout_step3_order_review, name='checkout_step3_order_review'),


	
	url(r'^promotion_products/$', views.promotion_products, name='promotion_products'),
	
	
	]
	
