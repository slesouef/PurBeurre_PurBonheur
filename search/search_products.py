"""
Custom module responsible for the search in the database of the user query

Args:
    User query as search term

Returns:
    List of hits ordered by nutritional rating
    Items in list contain the information necessary to build expected display
"""
from .models import Products


def get_suggestions(query):
    """
    Main method implementing the search algorithm

    :param query: User query term from request
    :return: the search result and 6 products from the same category ordered
    by rating
    """
    search = check_name(query)
    if not search.exists():
        search = check_contains(query)
        if not search.exists():
            raise LookupError
    result = search.first()
    category = get_category(result)
    products = get_products(category)
    return result, products


def check_name(query):
    """
    Check against product name in database for exact match

    :param query: user query from request
    :return: query items with name matching the query, if they exists
    """
    products = Products.objects.filter(name__exact=query)
    return products


def check_contains(query):
    """
    Check against product name in database with contains match

    :param query: user query from request
    :return: query items with name containing the query, if they exists
    """
    products = Products.objects.filter(name__icontains=query)
    return products


def get_category(product):
    """
    Get category object from the result of product search

    :param product: product returned from database search
    :return: category object from product search result
    """
    category = product.category
    return category


def get_products(category):
    """
    Get the 6 product from the category with the highest rating

    :param category: category object from product search result
    :return: 6 product objects from category with highest rating
    """
    products = Products.objects.filter(category=category).order_by('rating')[:6]
    return products
