""" View function for showing a user profile """
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from dashboard.models import Profile
from dashboard.forms import ProfileForm
from dashboard.utils import context_assign_user


logger = logging.getLogger(__name__)

@login_required(login_url='/dash/login/')
def show_profile(request, profile_uuid):
    """ Show user profile details and allow update settings and details """
    context = context_assign_user(request.user)
    context['profile_form'] = ProfileForm(instance=context['current_user'])
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            dark_mode = 'dark_mode' in request.POST
            Profile.objects.filter(pk=context['current_user'].id).update(bio=request.POST['bio'], dark_mode=dark_mode, iex_api_key=request.POST['iex_api_key'])
            messages.success(request, 'Your settings have been saved.')
            return redirect('dash:dashboard')
    return render(request, 'dash/users/show_profile.html', context)

def update_menu_session(request):
    """ Sets menu open or close in user session """
    print('setting menu sesson variable...')
    if not request.is_ajax() or not request.method == 'GET':
        return HttpResponseNotAllowed(['GET'])

    if request.path.split('/')[-1] == 'set_menu_status_closed':
        request.session['menuSetting'] = 'closed'
    else:
        request.session['menuSetting'] = 'open'
    return HttpResponse('Menu status set')
