from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from .forms import SignUpForm
from .models import MyUser
from search.models import Products


@never_cache
def signup(request):
    """
    The signup page must render the signup form when called with GET
    In case of a POST, the signup form is validated. If the form is valid,
    a user is created and authenticated. The view then returns a logged in
    session for the user's profile page
    """
    if request.user.is_authenticated:
        return redirect("profile")
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password")
                user.set_password(raw_password)
                user.save()
                authenticated_user = authenticate(request, username=username,
                                                  password=raw_password)
                login(request, authenticated_user)
                return redirect("profile")
        else:
            form = SignUpForm()
        return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    """
    Display the user's profile page with:
       user avatar
       user first_name
       user email address
    """
    context = {
        "avatar": False,
    }
    user = request.user
    first_name = user.get_short_name()
    context["first_name"] = first_name
    context["email"] = user.email
    context["avatar"] = user.avatar
    return render(request, "accounts/profile.html", context)


def save_favorite(request):
    """
    Allow user to create a new favorite entry in database.
    User must be authenticated or an error is raised.
    The favorite status of the product is checked and if not already a favorite
    the product is then added. Otherwise an error is returned.
    """
    if request.user.is_authenticated:
        userid = request.user.id
        favid = request.POST["product_id"]
        product = Products.objects.filter(id=favid).first()
        user = MyUser.objects.filter(id=userid).first()
        try:
            user.favorites.get(id=favid)
            response = {"error": "favorite already exists"}
        except Products.DoesNotExist:
            user.favorites.add(product)
            user.save()
            response = {"response": "OK"}
        return JsonResponse(response)
    else:
        raise PermissionDenied


@login_required
def favorites(request):
    """
    Display the user's list of favorites with:
        user avatar
        user full_name
    """
    context = {
        "avatar": False,
    }
    userid = request.user.id
    user = MyUser.objects.filter(id=userid).first()
    favs = user.favorites.all()
    context["user_name"] = user.get_full_name
    context["favorites"] = favs
    context["avatar"] = user.avatar
    return render(request, "accounts/favorites.html", context)
