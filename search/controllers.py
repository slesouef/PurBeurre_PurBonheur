"""
Module in charge of implementing the calls against the Open Food Facts API
using the openfoodfacts python module and inserting them in database
"""
import openfoodfacts

from .conf import PAGE_SIZE
from .models import Categories, Products, NutritionalValues


def get_data(query):
    """
    Search against Open Food Facts API using the openfoodfacts python
    module's advanced_search method

    :param query: user search term
    :return: dictionary object from API response
    """
    search_parameters = {"search_terms": query, "page_size": PAGE_SIZE}
    raw_data = openfoodfacts.products.advanced_search(search_parameters)
    return raw_data

def cleanup(data):
    """
    Method to make sure that all entries from Open Food Facts returned
    contain the necessary keys for treatment

    :param data: dictionary object retrieved from API response
    :return: list of valid entries from response
    """
    results = []
    search_results = data["products"]
    for item in search_results:
        if "categories" in item \
                and "product_name_fr" in item \
                and "brands" in item \
                and "quantity" in item \
                and "nutrition_grade_fr" in item \
                and "url" in item:
            results.append(item)
        else:
            pass
    return results

def save_data(data):
    """
    Method responsible for the insert of the valid entries retrieved from
    the API into the database

    :param data: List of valid entries to be saved
    """
    for item in data:
        raw_categories = item["categories"]
        categories = raw_categories.split(",")
        category = categories.pop()
        clean_cat = category.strip()
        check = Categories.objects.filter(name__exact=clean_cat)
        if not check.exists():
            c = Categories(name=clean_cat)
            c.save()
