from django.test import TestCase

from search import myrequests


EMPTY_SEARCH_RESPONSE = {"products": [], "page_size": "20", "count": 0,
                         "page": "1", "skip": 0}

MOCK_SEARCH_REPONSE = {"count": 7, "products": [
    {'brands': 'Ferrero,Nutella Biscuits',
     'categories': 'Biscuits cacaotés fourrés',
     'nutrition_grade_fr': 'e',
     'product_name_fr': 'Nutella Biscuits',
     'url': 'https://world.openfoodfacts.org/product/8000500310427/nutella'
            '-biscuits-ferrero',
     'quantity': 304},
    {'categories': 'Biscuits cacaotés fourrés',
     'nutrition_grade_fr': 'e',
     'product_name_fr': 'Nutella Biscuits',
     'url': 'https://world.openfoodfacts.org/product/8000500310427/nutella'
            '-biscuits-ferrero',
     'quantity': 304},
    {'brands': 'Ferrero,Nutella Biscuits',
     'nutrition_grade_fr': 'e',
     'product_name_fr': 'Nutella Biscuits',
     'url': 'https://world.openfoodfacts.org/product/8000500310427/nutella'
            '-biscuits-ferrero',
     'quantity': 304},
    {'brands': 'Ferrero,Nutella Biscuits',
     'categories': 'Biscuits cacaotés fourrés',
     'product_name_fr': 'Nutella Biscuits',
     'url': 'https://world.openfoodfacts.org/product/8000500310427/nutella'
            '-biscuits-ferrero',
     'quantity': 304},
    {'brands': 'Ferrero,Nutella Biscuits',
     'categories': 'Biscuits cacaotés fourrés',
     'nutrition_grade_fr': 'e',
     'url': 'https://world.openfoodfacts.org/product/8000500310427/nutella'
            '-biscuits-ferrero',
     'quantity': 304},
    {'brands': 'Ferrero,Nutella Biscuits',
     'categories': 'Biscuits cacaotés fourrés',
     'nutrition_grade_fr': 'e',
     'product_name_fr': 'Nutella Biscuits',
     'quantity': 304},
    {'brands': 'Ferrero,Nutella Biscuits',
     'categories': 'Biscuits cacaotés fourrés',
     'nutrition_grade_fr': 'e',
     'product_name_fr': 'Nutella Biscuits',
     'url': 'https://world.openfoodfacts.org/product/8000500310427/nutella'
            '-biscuits-ferrero'},
]}


# index page
class IndexPageTestCase(TestCase):
    """test that index page returns http 200"""

    def test_index_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


# legal mention page
class LegalPageTestCase(TestCase):
    """test that legal page returns http 200"""

    def test_legal_page(self):
        response = self.client.get('/legal/')
        self.assertEqual(response.status_code, 200)


# search result page
class SearchPageTestCase(TestCase):
    """test that search returns http 200"""

    def test_search_page(self):
        response = self.client.post('/search/', {'query': 'nutella'})
        self.assertEqual(response.status_code, 200)


# myrequests tests
class MyRequestsTestCase(TestCase):
    """test method to search on API"""

    @classmethod
    def setUpClass(cls):
        cls.search = myrequests.OpenFoodFactsData()

    # TODO: Figure out how to mock this shyte
    # def test_getdata_empty(self):
    #     """test when no hit is response"""
    #     cls.search.getdata("test")
    #     self.assertEqual(search.raw_data["count"], 0)
    #
    # def test_getdata_error(self):
    #     """test when error in API server"""
    #     cls.search.getdata("test")
    #     self.assertRaises(search.error_code, 500)
    #
    # def test_getdata_OK(self):
    #     """test when API response OK"""
    #     cls.search.getdata("test")
    #     self.assertEqual(search.raw_data["count"], 7)

    # test method to insert in DB??


# myproducts test
class MyProductsTestCase(TestCase):
    pass
# test method to search in db:
# test when query is name hit
# test when query is category hit and 6 items can be returned

# test when no hits or under 6 items in DB:

# test main method
# test when query has results
# test when query does NOT have results
# test method to filter search results
