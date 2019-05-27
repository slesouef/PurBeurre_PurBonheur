"""
Custom module responsible for the search in the database of the user query

Args:
    User query as search term

Returns:
    List of hits ordered by nutritional rating
    Items in list contain the information necessary to build expected display
"""
from .models import Categories, Products, NutritionalValues


class Suggestions:

    # main method returns 6 items to display
    def get_suggestions(self, query):
        pass
        # check name
           # if ok:
               # get category
               # get products
           # else:
               # check category
                   # if ok:
                       # get products
                   # else:
                       # check contains
                           # if ok:
                               # get category
                               # get products

    # methods to check in database
    # check against product name
    def check_name(self, query):
        """

        :param query: user query from request
        :return: the first item with name matching the query, if it exists
        """
        product = Products.objects.filter(name__exact=query).first()
        return product

    # check against product category
    def check_category(self, query):
        """

        :param query: user query from request
        :return: the first category with name matching the query, if it exists
        """
        category = Categories.objects.filter(name__exact=query).first()
        return category

    # check against name wildcard
    def check_contains(self, query):
        """

        :param query: user query from request
        :return: the first item with name containing the query, if it exists
        """
        product = Products.objects.filter(name__icontains=query).first()
        return product

    # get category
    def get_category(self, item):
        pass

    # get results for relevant category ordered by nutritional rating
    def get_products(self, query):
        pass
        # method to filter DB results
