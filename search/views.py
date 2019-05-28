from django.shortcuts import render

from .controllers import populate_database
from .search_products import get_suggestions



def index(request):
    return render(request, 'search/index.html')


def legal(request):
    return render(request, 'search/legal.html')


def search(request):
    query = request.POST.get('query')
    context ={}
    context['title'] = "Resultat de la recherche {}".format(query)
    try:
        products = get_suggestions(query)
        context['products'] = products
    except LookupError:
        try:
            populate_database(query)
            products = get_suggestions(query)
            context['products'] = products
        except ValueError:
            context['error'] = "Votre recherche n'a donne aucun resultats"
    return render(request, 'search/results.html', context)
