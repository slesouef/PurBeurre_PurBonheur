from django.test import TestCase
from unittest import mock

from search import controllers

MOCK_RESULT = {"products": [
    {
        "categories": "category",
        "product_name_fr": "name",
        "brands": "brand",
        "quantity": "quantity",
        "nutrition_grade_fr": "e",
        "url": "url",
    }
]}

INVALID_RESULTS = {"products": [
{
        "product_name_fr": "name",
        "brands": "brand",
        "quantity": "quantity",
        "nutrition_grade_fr": "e",
        "url": "url",
    },
{
        "categories": "category",
        "brands": "brand",
        "quantity": "quantity",
        "nutrition_grade_fr": "e",
        "url": "url",
    },
{
        "categories": "category",
        "product_name_fr": "name",
        "quantity": "quantity",
        "nutrition_grade_fr": "e",
        "url": "url",
    },
{
        "categories": "category",
        "product_name_fr": "name",
        "brands": "brand",
        "nutrition_grade_fr": "e",
        "url": "url",
    },
{
        "categories": "category",
        "product_name_fr": "name",
        "brands": "brand",
        "quantity": "quantity",
        "url": "url",
    },
{
        "categories": "category",
        "product_name_fr": "name",
        "brands": "brand",
        "quantity": "quantity",
        "nutrition_grade_fr": "e",
    }
]}

EMPTY_RESULTS = {"products": []}


@ mock.patch('search.controllers.openfoodfacts')
class TestControllers(TestCase):
    """Testing the search controllers module behaviour"""

    def test_call_api(self, mock_api):
        """Verify call API method returns the raw API results"""
        mock_api.products.advanced_search.return_value = INVALID_RESULTS
        results = controllers.call_api("query")
        self.assertEqual(len(results["products"]), 6)

    def test_cleanup_response_valid_entry(self, mock_api):
        """Verify that all valid results are returned"""
        results = controllers.cleanup_response(MOCK_RESULT)
        self.assertEqual(len(results), 1)

    def test_cleanup_response_invalid_entries(self, mock_api):
        """Verify that all invalid results are discarded"""
        results = controllers.cleanup_response(INVALID_RESULTS)
        self.assertEqual(len(results), 0)

    def test_populate_database_no_results(self, mock_api):
        """Verify that error is raised if the API does not return valid results"""
        mock_api.products.advanced_search.return_value = EMPTY_RESULTS
        with self.assertRaises(ValueError):
            controllers.populate_database("query")
