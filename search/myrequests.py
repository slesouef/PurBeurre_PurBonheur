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

    :returns: list of items with mandatory fields from API response
    """

    def __init__(self):
        self.raw_data = {}

    def getdata(self, query):
        """
        Search against API
        :param query: user search term
        """
        search_parameters = {"search_terms": query, "page_size": PAGE_SIZE}
        try:
            self.raw_data = openfoodfacts.products.advanced_search(
             search_parameters)
        except ConnectionError:
            # TODO: display error page
            print("error in search query")

    def cleanup(self):
        """
        Method to make sure that all entries from Open Food Facts returned
        contain the necessary keys for treatment

        :return: list of valid entries from response
        """
        results = []
        search_results = self.raw_data["products"]
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
