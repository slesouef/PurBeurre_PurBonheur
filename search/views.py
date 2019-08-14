from django.shortcuts import render

from .controllers import populate_database
from .search_products import get_suggestions
from .models import Products, NutritionalValues


def index(request):
    return render(request, "search/index.html")


def legal(request):
    return render(request, "search/legal.html")


def search(request):
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


def details(request, id):
    product = Products.objects.filter(id=id).first()
    nutrival = NutritionalValues.objects.filter(pid=id).first()
    nutriscore = f'/search/img/score/nutriscore-{product.rating}.svg'
    context = {
        "product": product,
        "nutrival": nutrival,
        "nutriscore": nutriscore
    }
    return render(request, "search/details.html", context)
