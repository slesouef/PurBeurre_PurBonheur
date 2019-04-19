from django.test import TestCase


# index page
class IndexPageTestCase(TestCase):
    # test that index page returns http 200
    def test_index_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


# legal mention page
class LegalPageTestCase(TestCase):
    # test that legal page returns http 200
    def test_legal_page(self):
        response = self.client.get('/legal/')
        self.assertEqual(response.status_code, 200)
