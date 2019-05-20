from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # TODO: user picture save at signup
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


@login_required()
def profile(request):
    context = {
        'avatar': None,
    }
    user = request.user
    first_name = user.get_short_name()
    context['first_name'] = first_name
    context['email'] = user.email
    return render(request, 'accounts/profile.html', context)


def logout(request):
    logout(request)
