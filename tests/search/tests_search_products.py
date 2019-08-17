from django.test import TestCase
from unittest.mock import patch, MagicMock

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
        product2 = Products(name='test')
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


class GetProductsTestCases(TestCase):
    """Verify that the method returns a query set object with the products
    from the category passed"""

    @patch('search.models.Products.objects.filter')
    def test_get_products(self, mock_db):
        category = Categories(name='test')
        product = Products(name='test')
        mock_db.return_value = MagicMock(
            side_effect=Products.objects.filter(category=category)
        )
        mock_db.return_value.order_by.return_value = [product]
        result = search_products.get_products(category)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result, list)
        mock_db.assert_called_with(category=category)
        mock_db.return_value.order_by.assert_called_with('rating')


class GetSuggestionTestCases(TestCase):
    """Verify that the main module method returns either a LookupError if no
    match for the query is found in database or a tuple of the found product
    and the suggested replacements"""

    @patch('search.search_products.get_products')
    @patch('search.search_products.check_name')
    def test_get_suggestion_check_name_hit(self, mock_search, mock_results):
        """Verify that if the check name method returns, get suggestions
        returns a tuple as well"""
        query_cat = Categories(name='test')
        query_result = Products(category=query_cat)
        mock_search.return_value = MagicMock(
            side_effect=Products.objects.filter(),
            return_value=query_result)
        mock_search.return_value.first.return_value = query_result
        mock_results.return_value = [query_result]
        result = search_products.get_suggestions('test')
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], Products)
        self.assertIsInstance(result[1], list)

    @patch('search.search_products.get_products')
    @patch('search.search_products.check_contains')
    @patch('search.search_products.check_name')
    def test_get_suggestion_check_contains_hit(self, mock_name, mock_contains,
                                               mock_results):
        """Verify that if the check contains method returns, get suggestions
        returns a tuple as well"""
        query_cat = Categories(name='test')
        empty_set = Products.objects.none()
        query_result = Products(category=query_cat)
        mock_name.return_value = empty_set
        mock_contains.return_value = MagicMock(
            side_effect=Products.objects.filter(),
            return_value=query_result)
        mock_contains.return_value.first.return_value = query_result
        mock_results.return_value = [query_result]
        result = search_products.get_suggestions('test')
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], Products)
        self.assertIsInstance(result[1], list)
