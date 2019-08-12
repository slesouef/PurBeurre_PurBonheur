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
    },
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

INVALID_RESULTS = {"products": []}


@mock.patch('search.controllers.openfoodfacts')
class TestControllers(TestCase):
    """Testing the search controllers module behaviour"""

    def test_call_api(self, mock_api):
        """Testing call api method"""
        mock_api.products.advanced_search.return_value = MOCK_RESULT
        results = controllers.call_api("query")
        self.assertEqual(len(results["products"]), 7)

    def test_cleanup_response(self, mock_api):
        """Verify that all invalid results are discarded"""
        results = controllers.cleanup_response(MOCK_RESULT)
        self.assertEqual(len(results), 1)

    def test_populate_database_no_results(self, mock_api):
        """Verify that error is raised if the API does not return valid results"""
        mock_api.products.advanced_search.return_value = INVALID_RESULTS
        with self.assertRaises(ValueError):
            controllers.populate_database("query")
