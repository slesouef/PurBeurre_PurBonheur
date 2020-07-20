"""
Module in charge of implementing the calls against the Open Food Facts API
using the openfoodfacts python module and inserting them in database
"""
import openfoodfacts

from .conf import PAGE_SIZE
from .models import Categories, Products, NutritionalValues


def populate_database(query):
    """
    Main method to insert results from user query search in database

    :param query: user search term
    """
    raw = call_api(query)
    clean = cleanup_response(raw)
    if not clean:
        raise ValueError
    else:
        save_data(clean)


def call_api(query):
    """
    Search against Open Food Facts API using the openfoodfacts python
    module's advanced_search method

    :param query: user search term
    :return: dictionary object from API response
    """
    search_parameters = {"search_terms": query,
                         "page_size": PAGE_SIZE,
                         "cc": "fr",
                         "lc": "fr"
                         }
    raw_data = openfoodfacts.products.advanced_search(search_parameters)
    return raw_data


def cleanup_response(data):
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
            cat = c
        else:
            cat = check.first()
        name = item["product_name_fr"]
        brand = item["brands"]
        quantity = item["quantity"]
        rating = item["nutrition_grade_fr"]
        url = item["url"]
        code = item["code"]
        p = Products(name=name, brand=brand, quantity=quantity,
                     rating=rating, url=url, code=code, category=cat)
        if "image_url" in item:
            image = item["image_url"]
            p.image = image
        p.save()
        v = NutritionalValues()
        v.pid = p
        if "serving_size" in item:
            v.serving_size = item["serving_size"]
        if "energy_serving" in item["nutriments"]:
            v.energy = item["nutriments"]["energy_serving"]
        if "energy_100g" in item["nutriments"]:
            v.energy_per100 = item["nutriments"]["energy_100g"]
        if "energy_unit" in item["nutriments"]:
            v.energy_unit = item["nutriments"]["energy_unit"]
        if "fat_serving" in item["nutriments"]:
            v.fat = item["nutriments"]["fat_serving"]
        if "fat_100g" in item["nutriments"]:
            v.fat_per100 = item["nutriments"]["fat_100g"]
        if "fat_unit" in item["nutriments"]:
            v.fat_unit = item["nutriments"]["fat_unit"]
        if "saturated-fat_serving" in item["nutriments"]:
            v.saturatedFat = item["nutriments"]["saturated-fat_serving"]
        if "saturated-fat_100g" in item["nutriments"]:
            v.saturatedFat_per100 = item["nutriments"]["saturated-fat_100g"]
        if "saturated-fat_unit" in item["nutriments"]:
            v.saturatedFat_unit = item["nutriments"]["saturated-fat_unit"]
        if "carbohydrates_serving" in item["nutriments"]:
            v.carbohydrates = item["nutriments"]["carbohydrates_serving"]
        if "carbohydrates_100g" in item["nutriments"]:
            v.carbohydrates_per100 = item["nutriments"]["carbohydrates_100g"]
        if "carbohydrates_unit" in item["nutriments"]:
            v.carbohydrates_unit = item["nutriments"]["carbohydrates_unit"]
        if "sugars_serving" in item["nutriments"]:
            v.sugar = item["nutriments"]["sugars_serving"]
        if "sugars_100g" in item["nutriments"]:
            v.sugar_per100 = item["nutriments"]["sugars_100g"]
        if "sugars_unit" in item["nutriments"]:
            v.sugar_unit = item["nutriments"]["sugars_unit"]
        if "fiber_serving" in item["nutriments"]:
            v.fiber = item["nutriments"]["fiber_serving"]
        if "fiber_100g" in item["nutriments"]:
            v.fiber_per100 = item["nutriments"]["fiber_100g"]
        if "fiber_unit" in item["nutriments"]:
            v.fiber_unit = item["nutriments"]["fiber_unit"]
        if "proteins_serving" in item["nutriments"]:
            v.proteins = item["nutriments"]["proteins_serving"]
        if "proteins_100g" in item["nutriments"]:
            v.proteins_per100 = item["nutriments"]["proteins_100g"]
        if "proteins_unit" in item["nutriments"]:
            v.proteins_unit = item["nutriments"]["proteins_unit"]
        if "salt_serving" in item["nutriments"]:
            v.salt = item["nutriments"]["salt_serving"]
        if "salt_100g" in item["nutriments"]:
            v.salt_per100 = item["nutriments"]["salt_100g"]
        if "salt_unit" in item["nutriments"]:
            v.salt_unit = item["nutriments"]["salt_unit"]
        v.save()
