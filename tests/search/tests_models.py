from django.test import TestCase

from search.models import Products


class ProductModelTestCase(TestCase):
    """Test the get_absolute_url method from the Products model"""

    def test_get_absolute_url(self):
        """
        Verify that the url returned by the method contains the product id
        """
        product = Products()
        product.id = 10
        url = product.get_absolute_url()
        self.assertIn("10", url)
