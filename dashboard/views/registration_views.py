from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        signup_form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': signup_form})


