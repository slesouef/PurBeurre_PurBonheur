from django.test import TestCase
from unittest import mock

from search import controllers
from search.models import Products, Categories, NutritionalValues

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


class TestControllers(TestCase):
    """Testing the search controllers module behaviour"""

    @mock.patch("search.controllers.openfoodfacts")
    def test_call_api(self, mock_api):
        """Verify call API method returns the raw API results"""
        mock_api.products.advanced_search.return_value = INVALID_RESULTS
        results = controllers.call_api("query")
        self.assertEqual(len(results["products"]), 6)

    def test_cleanup_response_valid_entry(self):
        """Verify that a valid results is returned"""
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
            }
        ]
        }
        results = controllers.cleanup_response(mock_result)
        self.assertEqual(len(results), 1)

    def test_cleanup_response_invalid_entries(self):
        """Verify that all invalid results are discarded"""
        results = controllers.cleanup_response(INVALID_RESULTS)
        self.assertEqual(len(results), 0)

    @mock.patch("search.controllers.openfoodfacts")
    def test_populate_database_no_results(self, mock_api):
        """Verify that error is raised if the API does not return valid
        results"""
        empty_result = {"products": []}
        mock_api.products.advanced_search.return_value = empty_result
        with self.assertRaises(ValueError):
            controllers.populate_database("query")

    @mock.patch("search.controllers.openfoodfacts")
    def test_populate_database(self, mock_api):
        """
        Verify that an item is created in database if the API response
        contains a valid item
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {}
            }
        ]}
        mock_api.products.advanced_search.return_value = mock_result
        controllers.populate_database("query")
        saved_item = Products.objects.all()
        self.assertEqual(len(saved_item), 1)

    def test_save_data_minimal(self):
        """
        Verify that an item is created in database if only required fields
        are available
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {}
            }
        ]}
        pre_cat = Categories.objects.all()
        self.assertEqual(len(pre_cat), 0)
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        post_cat = Categories.objects.all()
        self.assertEqual(len(post_cat), 1)
        self.assertTrue(saved_item.category, "category")
        self.assertTrue(saved_item.name, "name")
        self.assertTrue(saved_item.brand, "brand")
        self.assertTrue(saved_item.quantity, "quantity")
        self.assertTrue(saved_item.rating, "e")
        self.assertTrue(saved_item.url, "url")

    def test_save_data_category_exists(self):
        """
        Verify that if the category exists, no new category is created
        when an item is created
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {}
            }
        ]}
        Categories.objects.create(name="category")
        controllers.save_data(mock_result["products"])
        categories = Categories.objects.all()
        self.assertEqual(len(categories), 1)

    def test_save_data_with_image(self):
        """
        Verify that an item is created in database with an image if the
        image url is available in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "image_url": "image_url",
                "code": "code",
                "nutriments": {}
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        self.assertTrue(saved_item.image, "image_url")

    def test_save_data_with_serving_size(self):
        """
        Verify that an item is created in database with a nutritional
        value serving size if the field serving size is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "serving_size": "serving_size",
                "nutriments": {}
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.serving_size, "serving_size")

    def test_save_data_with_energy_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value energy field if the field energy serving is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "energy_serving": "energy_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.energy, "energy_serving")

    def test_save_data_with_energy_100(self):
        """
        Verify that an item is created in database with a nutritional
        value energy per 100 field if the field energy 100g is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "energy_100g": "energy_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.energy_per100, "energy_100g")

    def test_save_data_with_energy_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value energy unit field if the field energy unit is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "energy_unit": "energy_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.energy_unit, "energy_unit")

    def test_save_data_with_fat_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value fat serving field if the field fat serving is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "fat_serving": "fat_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.fat, "fat_serving")

    def test_save_data_with_fat_100(self):
        """
        Verify that an item is created in database with a nutritional
        value fat per 100 field if the field fat 100g is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "fat_100g": "fat_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.fat_per100, "fat_100g")

    def test_save_data_with_fat_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value fat unit field if the field fat unit is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "fat_unit": "fat_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.fat_unit, "fat_unit")

    def test_save_data_with_saturated_fat_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value saturated fat serving field if the field saturated fat serving
        is available in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "saturated-fat_serving": "saturated-fat_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.saturatedFat, "saturated-fat_serving")

    def test_save_data_with_saturated_fat_100(self):
        """
        Verify that an item is created in database with a nutritional
        value saturated fat per 100 field if the field saturated fat 100g
        is available in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "saturated-fat_100g": "saturated-fat_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.saturatedFat_per100, "saturated-fat_100g")

    def test_save_data_with_saturated_fat_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value saturated fat unit field if the field saturated fat unit is
        available in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "saturated-fat_unit": "saturated-fat_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.saturatedFat_unit, "saturated-fat_unit")

    def test_save_data_with_carbohydrates_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value carbohydrates serving field if the field carbohydrates serving
        is available in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "carbohydrates_serving": "carbohydrates_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.carbohydrates, "carbohydrates_serving")

    def test_save_data_with_carbohydrates_100(self):
        """
        Verify that an item is created in database with a nutritional
        value carbohydrates per 100 field if the field carbohydrates 100g
        is available in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "carbohydrates_100g": "carbohydrates_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.carbohydrates_per100, "carbohydrates_100g")

    def test_save_data_with_carbohydrates_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value carbohydrates unit field if the field carbohydrates unit is
        available in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "carbohydrates_unit": "carbohydrates_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.carbohydrates_unit, "carbohydrates_unit")

    def test_save_data_with_sugars_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value sugars serving field if the field sugars serving is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "sugars_serving": "sugars_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.sugar, "sugars_serving")

    def test_save_data_with_sugars_100(self):
        """
        Verify that an item is created in database with a nutritional
        value sugars per 100 field if the field sugars 100g is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "sugars_100g": "sugars_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.sugar_per100, "sugars_100g")

    def test_save_data_with_sugars_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value sugars unit field if the field sugars unit is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "sugars_unit": "sugars_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.sugar_unit, "sugars_unit")

    def test_save_data_with_fiber_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value fiber serving field if the field fiber serving is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "fiber_serving": "fiber_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.fiber, "fiber_serving")

    def test_save_data_with_fiber_100(self):
        """
        Verify that an item is created in database with a nutritional
        value fiber per 100 field if the field fiber 100g is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "fiber_100g": "fiber_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.fiber_per100, "fiber_100g")

    def test_save_data_with_fiber_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value fiber unit field if the field fiber unit is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "fiber_unit": "fiber_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.fiber_unit, "fiber_unit")

    def test_save_data_with_proteins_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value proteins serving field if the field proteins serving is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "proteins_serving": "proteins_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.proteins, "proteins_serving")

    def test_save_data_with_proteins_100(self):
        """
        Verify that an item is created in database with a nutritional
        value proteins per 100 field if the field proteins 100g is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "proteins_100g": "proteins_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.proteins_per100, "proteins_100g")

    def test_save_data_with_proteins_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value proteins unit field if the field proteins unit is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "proteins_unit": "proteins_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.proteins_unit, "proteins_unit")

    def test_save_data_with_salt_serving(self):
        """
        Verify that an item is created in database with a nutritional
        value salt serving field if the field salt serving is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "salt_serving": "salt_serving"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.salt, "salt_serving")

    def test_save_data_with_salt_100(self):
        """
        Verify that an item is created in database with a nutritional
        value salt per 100 field if the field salt 100g is available
        in API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "salt_100g": "salt_100g"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.salt_per100, "salt_100g")

    def test_save_data_with_salt_unit(self):
        """
        Verify that an item is created in database with a nutritional
        value salt unit field if the field salt unit is available in
        API response
        """
        mock_result = {"products": [
            {
                "categories": "category",
                "product_name_fr": "name",
                "brands": "brand",
                "quantity": "quantity",
                "nutrition_grade_fr": "e",
                "url": "url",
                "code": "code",
                "nutriments": {
                    "salt_unit": "salt_unit"
                }
            }
        ]}
        controllers.save_data(mock_result["products"])
        saved_item = Products.objects.all().first()
        nutrival = NutritionalValues.objects.filter(pid=saved_item.id).first()
        self.assertTrue(nutrival.salt_unit, "salt_unit")
