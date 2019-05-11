from django.shortcuts import render

from .myrequests import OpenFoodFactsData
from .models import Products, Categories



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
    if not products.exists():
        response = OpenFoodFactsData()
        response.getdata(query)
        response.cleanup()
        product = {}
        products = []
        for item in response.results:
            product['name'] = item['product_name']
            products.append(product.copy())
    title = "Resultat de la recherche {}".format(query)
    context = {
        'products': products,
        'title': title
    }
    return render(request, 'search/results.html', context)
