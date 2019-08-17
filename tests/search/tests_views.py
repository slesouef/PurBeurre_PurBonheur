from django.test import TestCase
from unittest.mock import patch, MagicMock


class IndexPageTestCase(TestCase):
    """test that index page returns http 200"""

    def test_index_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/base.html')
        self.assertTemplateUsed(response, 'search/search_form.html')
        self.assertTemplateUsed(response, 'search/index.html')


class LegalPageTestCase(TestCase):
    """test that legal page returns http 200"""

    def test_legal_page(self):
        response = self.client.get('/legal/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/base.html')
        self.assertTemplateUsed(response, 'search/search_form.html')
        self.assertTemplateUsed(response, 'search/legal.html')


class SearchPageTestCase(TestCase):
    """test that search returns http 200"""

    @patch('search.views.get_suggestions')
    def test_search_page_item_in_database(self, mock_search):
        mock_search.return_value = {'result': 'result', 'products': 'products'}
        response = self.client.post('/search/', {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/base.html')
        self.assertTemplateUsed(response, 'search/search_form.html')
        self.assertTemplateUsed(response, 'search/results_page.html')
        self.assertTemplateUsed(response, 'search/result.html')
        self.assertEqual(response.context['result'], 'result')
        self.assertEqual(response.context['products'], 'products')

    @patch('search.views.get_suggestions')
    @patch('search.views.populate_database')
    def test_search_page_item_not_in_database(self, mock_api, mock_search):
        mock_search.side_effect = [LookupError, {'result': 'result',
                                                 'products': 'products'}]
        response = self.client.post('/search/', {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/base.html')
        self.assertTemplateUsed(response, 'search/search_form.html')
        self.assertTemplateUsed(response, 'search/results_page.html')
        self.assertTemplateUsed(response, 'search/result.html')
        self.assertEqual(response.context['result'], 'result')
        self.assertEqual(response.context['products'], 'products')

    @patch('search.views.get_suggestions')
    @patch('search.views.populate_database')
    def test_search_page_no_results(self, mock_api, mock_search):
        mock_search.side_effect = [LookupError, ValueError]
        response = self.client.post('/search/', {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/base.html')
        self.assertTemplateUsed(response, 'search/search_form.html')
        self.assertTemplateUsed(response, 'search/results_page.html')
        self.assertTemplateNotUsed(response, 'search/result.html')
        self.assertEqual(response.context['error'],
                         "Votre recherche n'a donné aucun résultats")
