from django.shortcuts import render
# from django.http import HttpResponse

from .models import Products, Categories


# Create your views here.
def index(request):
    return render(request, 'search/index.html')


def legal(request):
    return render(request, 'search/legal.html')


def search(request):
    query = request.POST.get('query')
    products = Products.objects.filter(name__icontains=query)
    if not products.exists():
        products = Products.objects.filter(brand__icontains=query)
    if not products.exists():
        products = Categories.objects.filter(name__icontains=query)
    title = "Resultat de la recherche {}".format(query)
    context = {
        'products': products,
        'title': title
    }
    return render(request, 'search/results.html', context)
