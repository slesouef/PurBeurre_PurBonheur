"""
Module in charge of implementing the calls against the Open Food Facts API
using the openfoodfacts python module
"""
import openfoodfacts

from .conf import PAGE_SIZE


class OpenFoodFactsData:
    """
    Class containing the raw information retrieved from Open Food Facts
    API

    Returns:
        JSON formatted object
    """

    def __init__(self):
        self.raw_data = {}
        self.results = []

    def getdata(self, query):
        """
        Search against API
        :param query: user search term
        :return: json formatted object
        """
        search_parameters = {"search_terms": query, "page_size": PAGE_SIZE}
        try:
            self.raw_data = openfoodfacts.products.advanced_search(
             search_parameters)
        except ConnectionError:
            # TODO: display HTTP 500 page
            print("page_500")

    def cleanup(self):
        """
        Method to make sure that all entries from Open Food Facts returned
        contain the necessary keys for treatment

        :return: list of valid entries from response
        """
        search_results = self.raw_data["products"]
        for item in search_results:
            try:
                item["categories"]
                item["nutrition_grade_fr"]
                item["product_name_fr"]
                item["brands"]
                item["url"]
                item["quantity"]
                self.results.append(item)
            except KeyError:
                pass
