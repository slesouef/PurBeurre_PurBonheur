"""PurBeurre_PurBonheur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from search import views as search_views
from accounts import views as account_views

urlpatterns = [
    path('', search_views.index, name='index'),
    path('legal/', search_views.legal, name='legal'),
    path('search/', search_views.search, name='search'),
    path('details/<int:pid>/', search_views.details, name='details'),
    path('accounts/login/',
         auth_views.LoginView.as_view(redirect_authenticated_user=True),
         name='login'),
    path('accounts/signup/', account_views.signup, name='signup'),
    path('accounts/profile/', account_views.profile, name='profile'),
    path('accounts/favorites/new/',
         account_views.save_favorite, name='save_favorite'),
    path('accounts/favorites/', account_views.favorites, name='favorites'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
