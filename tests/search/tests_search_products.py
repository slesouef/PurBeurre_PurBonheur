from django.test import TestCase
from unittest.mock import patch

from search import search_products
from search.models import Products, Categories


class CheckNameTestCases(TestCase):
    """Verify that the check_name method returns a query object with the
    products in database whose name are an exact match to the query"""

    @patch('search.models.Products.objects.filter')
    def test_check_name_no_hits(self, mock_db):
        """Verify that the check_name method returns an empty query set if no
        matches are found"""
        empty_set = Products.objects.none()
        mock_db.return_value = empty_set
        results = search_products.check_name('test')
        self.assertEqual(len(results), 0)

    @patch('search.models.Products.objects.filter')
    def test_check_name_with_hit(self, mock_db):
        """Verify that the method returns the query set if a hit is found"""
        product1 = Products(name='test')
        mock_db.return_value = [product1]
        results = search_products.check_name('test')
        self.assertEqual(len(results), 1)
        product2 = Products(name='test')
        mock_db.return_value = [product1, product2]
        results = search_products.check_name('test')
        self.assertEqual(len(results), 2)


class CheckContainsTestCases(TestCase):
    """Verify that the check_contains method returns a query object with the
    products in database whose name are a possible match to the query"""

    @patch('search.models.Products.objects.filter')
    def test_check_contains_no_hits(self, mock_db):
        """Verify that the check_contains method returns an empty query set
        if no matches are found"""
        empty_set = Products.objects.none()
        mock_db.return_value = empty_set
        results = search_products.check_contains('test')
        self.assertEqual(len(results), 0)

    @patch('search.models.Products.objects.filter')
    def test_check_contains_with_hit(self, mock_db):
        """Verify that the method returns the query set if a hit is found"""
        product1 = Products(name='test')
        mock_db.return_value = [product1]
        results = search_products.check_contains('test')
        self.assertEqual(len(results), 1)
        product2 = Products(name='tes')
        mock_db.return_value = [product1, product2]
        results = search_products.check_contains('test')
        self.assertEqual(len(results), 2)


class GetCategoryTestCases(TestCase):
    """Verify that the method returns the category of a product"""

    def test_get_category(self):
        """A product's category is return when the product is passed to the
        method"""
        category = Categories(name='test_category')
        product = Products(category=category)
        result = search_products.get_category(product)
        self.assertEqual(result.name, 'test_category')
        self.assertIsInstance(result, Categories)
