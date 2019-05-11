"""
Custom module responsible for the search in the database of the user query

Args:
    User query as search term

Returns:
    List of hits ordered by nutritional rating
    Items in list contain the information necessary to build expected display
"""
import openfoodfacts

from .conf import PAGE_SIZE
from .models import Categories, Products, NutritionalValues


class Results():

    pass
# main method returns 6 items to display

# method to check in database
    # check against product name
    # check against product brand
    # check against product category

# method to make API call if no DB hits
    # create call URL
    # make API call

# method to insert API results in DB

# method to filter DB or API results
    #