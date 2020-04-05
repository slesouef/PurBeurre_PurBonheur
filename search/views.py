import logging

from django.shortcuts import render

from .controllers import populate_database
from .search_products import get_suggestions
from .models import Products, NutritionalValues

logger = logging.getLogger(__name__)


def index(request):
    """Site landing page"""
    return render(request, "search/index.html")


def legal(request):
    """Display legal information page"""
    return render(request, "search/legal.html")


def search(request):
    """
    Display the product search results
    The response must contain a title with the query term used for the search.
    If the search is successful, a product and its substitutes are provided
    in the response. Otherwise, an error is provided
    """
    query = request.POST.get("query")
    context = {"title": "Résultat de la recherche {}".format(query)}
    try:
        result, products = get_suggestions(query)
        context["result"] = result
        context["products"] = products
    except LookupError:
        try:
            populate_database(query)
            result, products = get_suggestions(query)
            context["result"] = result
            context["products"] = products
        except (ValueError, LookupError):
            context["error"] = "Votre recherche n'a donné aucun résultats"
    return render(request, "search/results_page.html", context)


def details(request, pid):
    """
    Display the detailed information of a Product:
        the product itself
        the nutritional values associated with that product
        the nutriscore image for this product's rating
    """
    product = Products.objects.filter(id=pid).first()
    nutrival = NutritionalValues.objects.filter(pid=pid).first()
    nutriscore = f'/search/img/score/nutriscore-{product.rating}.svg'
    context = {
        "product": product,
        "nutrival": nutrival,
        "nutriscore": nutriscore
    }
    return render(request, "search/details.html", context)
