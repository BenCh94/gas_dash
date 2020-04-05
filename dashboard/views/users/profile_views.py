""" View function for showing a user profile """
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from dashboard.models import Profile
from dashboard.utils import context_assign_user


logger = logging.getLogger(__name__)

@login_required(login_url='/dash/login/')
def show_profile(request, profile_id):
    """ Show user profile details and allow update settings and details """
    context = context_assign_user(request.user)
    # profile_object = get_object_or_404(Profile, pk=profile_id)
    return render(request, 'dash/users/show_profile.html', context)

def update_menu_session(request):
    """ Sets menu open or close in user session """
    print('setting menu sesson variable')
    if not request.is_ajax() or not request.method == 'GET':
        return HttpResponseNotAllowed(['GET'])

    if request.path.split('/')[-1] == 'set_menu_status_closed':
        request.session['menuSetting'] = 'closed'
    else:
        request.session['menuSetting'] = 'open'
    return HttpResponse('Menu status set')
