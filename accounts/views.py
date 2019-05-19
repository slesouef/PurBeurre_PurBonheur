from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()
            authenticated_user = authenticate(request, username=username,
                                 password=raw_password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('profile')
            else:
                user.delete()
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
