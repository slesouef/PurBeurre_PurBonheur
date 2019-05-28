from django.shortcuts import render

from .controllers import populate_database
from .models import Products, Categories



def index(request):
    return render(request, 'search/index.html')


def legal(request):
    return render(request, 'search/legal.html')


def search(request):
    query = request.POST.get('query')
    results = Products.objects.filter(name__icontains=query)
    if not results.exists():
        results = Products.objects.filter(brand__icontains=query)
    if not results.exists():
        populate_database(query)
        results = Products.objects.filter(name__icontains=query)
        if not results.exists():
            results = Products.objects.filter(brand__icontains=query)
    category = results.first().category
    products = Products.objects.filter(category=category).order_by('rating')[:6]
    # product_list = []
    # for entry in products:
    #     name = entry.name
    #     print(name)
    #     product_list.append(name)
    title = "Resultat de la recherche {}".format(query)
    context = {
        'products': products,
        'title': title
    }
    return render(request, 'search/results.html', context)
