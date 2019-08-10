from django.test import TestCase
from unittest.mock import patch, MagicMock


class IndexPageTestCase(TestCase):
    """test that index page returns http 200"""

    def test_index_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):
    """test that legal page returns http 200"""

    def test_legal_page(self):
        response = self.client.get('/legal/')
        self.assertEqual(response.status_code, 200)


class SearchPageTestCase(TestCase):
    """test that search returns http 200"""

    @patch('search.views.search_products')
    def test_search_page(self, mock_search):
        mock_search.get_suggestions.return_value = {'result': 'result', 'products': 'products'}
        response = self.client.post('/search/', {'query': 'nutella'})
        self.assertEqual(response.status_code, 200)
