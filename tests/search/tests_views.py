from django.test import TestCase
from unittest.mock import patch, MagicMock

from search.models import Products, NutritionalValues


class SearchViewsTestCase(TestCase):

    def test_index_page(self):
        """test that index page returns http 200"""
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "search/index.html")

    def test_legal_page(self):
        """test that legal page returns http 200"""
        response = self.client.get("/legal/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "search/legal.html")

    @patch("search.views.get_suggestions")
    def test_search_page_item_in_database(self, mock_search):
        """
         Verify that the search page returns the correct context if
        the search has found a query hit in database

        :param mock_search: mock search_products module response
        """
        mock_search.return_value = {"result": "result", "products": "products"}
        response = self.client.post("/search/", {"query": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "search/results_page.html")
        self.assertTemplateUsed(response, "search/result.html")
        self.assertEqual(response.context["result"], "result")
        self.assertEqual(response.context["products"], "products")

    @patch("search.views.get_suggestions")
    @patch("search.views.populate_database")
    def test_search_page_item_not_in_database(self, mock_api, mock_search):
        """
        Verify that the search page returns the correct context if
        the search could not find a query hit in database before the query is
        run against the OpenFoodFacts API but a hit occurs after

        :param mock_api: mock controllers module. does not return.
        :param mock_search: mock search_products module response
        """
        mock_search.side_effect = [LookupError, {"result": "result",
                                                 "products": "products"}]
        response = self.client.post("/search/", {"query": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "search/results_page.html")
        self.assertTemplateUsed(response, "search/result.html")
        self.assertEqual(response.context["result"], "result")
        self.assertEqual(response.context["products"], "products")

    @patch("search.views.get_suggestions")
    @patch("search.views.populate_database")
    def test_search_page_no_API_results(self, mock_api, mock_search):
        """
        Verify that the search page returns the correct context if
        the search could not find a query hit in database and the API call
        does not return new products to insert in database

        :param mock_api: mock controllers module. does not return.
        :param mock_search: mock search_products module response
        """
        mock_search.side_effect = [LookupError, ValueError]
        response = self.client.post("/search/", {"query": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "search/results_page.html")
        self.assertTemplateNotUsed(response, "search/result.html")
        self.assertEqual(response.context["error"],
                         "Votre recherche n'a donné aucun résultats")

    @patch("search.views.get_suggestions")
    @patch("search.views.populate_database")
    def test_search_page_no_DB_results(self, mock_api, mock_search):
        """
        Verify that the search page returns the correct context if
        the search could not find a query hit in database even after
        the call against the OpenFoodFacts API added new products in database

        :param mock_api: mock controllers module. does not return.
        :param mock_search: mock search_products module response
        """
        mock_search.side_effect = [LookupError, LookupError]
        response = self.client.post("/search/", {"query": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "search/results_page.html")
        self.assertTemplateNotUsed(response, "search/result.html")
        self.assertEqual(response.context["error"],
                         "Votre recherche n'a donné aucun résultats")

    @patch("search.models.NutritionalValues.objects.filter")
    @patch("search.models.Products.objects.filter")
    def test_details(self, mock_product, mock_nutrival):
        """
        Verify that the details page returns the following information on a
        product:
            the product object
            the nutritional values associated to this product
            the correct nutriscore image based on product rating

        :param mock_product: mock the query against Products table
        :param mock_nutrival: mock the search against NutritionalValues table
        """
        mock_product.return_value = MagicMock(
            side_effect=Products.objects.filter()
        )
        mock_product.return_value.first.return_value = Products(rating="a")
        mock_nutrival.return_value = MagicMock(
            side_effect=Products.objects.filter()
        )
        mock_nutrival.return_value.first.return_value = NutritionalValues()
        response = self.client.get("/details/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "search/details.html")
        self.assertIsInstance(response.context["product"], Products)
        self.assertIsInstance(response.context["nutrival"], NutritionalValues)
        self.assertIn("nutriscore-a", response.context["nutriscore"])
