from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import authenticate, login
from ..forms import SignUpForm, LoginForm
from ..views import dash_views

def signup(request):
    errors = {}
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            username = request.POST.get('username')
            raw_password = request.POST.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                if request.GET:
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('/dash')
            else:
                errors['error'] = form.errors
        elif request.POST.get('submit') == 'signup':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/dash')
            else:
                errors['error'] = form.errors
    signup_form = SignUpForm()
    login_form = LoginForm()
    print(errors)
    return render(request, 'registration/login.html', {'signup_form': signup_form, 'login_form': login_form, 'errors': errors, 'page': 'register'})


def login_view(request):
    errors = {}
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            username = request.POST.get('username')
            raw_password = request.POST.get('password')
            user = authenticate(request, username=username, password=raw_password)
            form = LoginForm(request.POST)
            if user is not None:
                login(request, user)
                if request.GET:
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('/dash')
            else:
                errors['error'] = "Invalid username or password"
        elif request.POST.get('submit') == 'signup':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/dash')
            else:
                errors['error'] = form.errors
    signup_form = SignUpForm()
    login_form = LoginForm()
    return render(request, 'registration/login.html', {'signup_form': signup_form, 'login_form': login_form, 'errors': errors, 'page': 'login'})    

