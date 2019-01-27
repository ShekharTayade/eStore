from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Count

from datetime import datetime
import datetime
import json

from django.contrib.auth.models import User

from eStore.models import Ecom_site, Profile, Profile_group


from .frame_views import *

today = datetime.date.today()

def profile_group(request):

	return render(request, "eStore/architect_registration.html", {})
	