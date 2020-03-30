# View function for showing a user profile
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import Profile


logger = logging.getLogger(__name__)

@login_required(login_url='/dash/login/')
def show_profile(request, profile_id):
    context = dict()
    context['current_user'] = request.user.profile
    profile_object = get_object_or_404(Profile, pk=profile_id)
    return render(request, 'dash/users/show_profile.html', context)

