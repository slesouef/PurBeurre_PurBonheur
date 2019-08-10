from django.test import TestCase
from unittest import mock


@mock.patch('search.controllers.openfoodfacts')
class TestControllers(TestCase):
    """Testing the search controllers module behaviour"""

    def test_call_api(self, mock_opff):
        """testing call api method"""
        pass
