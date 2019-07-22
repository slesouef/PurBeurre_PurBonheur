from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.http import JsonResponse

from .forms import SignUpForm
from .models import MyUser
from search.models import Products


@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
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


@login_required
def profile(request):
    context = {
        'avatar': None,
    }
    user = request.user
    first_name = user.get_short_name()
    context['first_name'] = first_name
    context['email'] = user.email
    return render(request, 'accounts/profile.html', context)


@login_required
def save_favorite(request):
    userid = request.user.id
    favid = request.POST['product_id']
    product = Products.objects.filter(id=favid).first()
    user = MyUser.objects.filter(id=userid).first()
    try:
        user.favorites.get(id=favid)
        response = {'error': 'Ce produit est deja sauvegarder'}
    except Products.DoesNotExist:
        user.favorites.add(product)
        user.save()
        response = {'reponse': 'OK'}
    return JsonResponse(response)


def logout(request):
    logout(request)
