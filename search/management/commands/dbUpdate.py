import openfoodfacts
import logging

from django.core.management.base import BaseCommand

from search.models import Products, NutritionalValues

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update all entries in the database with the current OpenFoodFacts information"

    def handle(self, *agrs, **options):
        for product in Products.objects.all():
            if product.code is not None:
                response = openfoodfacts.products.get_product(product.code)
                if response["status"] == 1:
                    item = response["product"]
                    if "product_name_fr" in item:
                        product.name = item["product_name_fr"]
                    if "brands" in item:
                        product.brand = item["brands"]
                    if "quantity" in item:
                        product.quantity = item["quantity"]
                    if "nutrition_grade_fr" in item:
                        product.rating = item["nutrition_grade_fr"]
                    if "url" in item:
                        product.url = item["url"]
                    product.code = item["code"]
                    if "image_url" in item:
                        product.image = item["image_url"]
                    nutri_val = NutritionalValues.objects.filter(pid=product)
                    if "serving_size" in item:
                        nutri_val.serving_size = item["serving_size"]
                    if "energy_serving" in item["nutriments"]:
                        nutri_val.energy = item["nutriments"]["energy_serving"]
                    if "energy_100g" in item["nutriments"]:
                        nutri_val.energy_per100 = item["nutriments"]["energy_100g"]
                    if "energy_unit" in item["nutriments"]:
                        nutri_val.energy_unit = item["nutriments"]["energy_unit"]
                    if "fat_serving" in item["nutriments"]:
                        nutri_val.fat = item["nutriments"]["fat_serving"]
                    if "fat_100g" in item["nutriments"]:
                        nutri_val.fat_per100 = item["nutriments"]["fat_100g"]
                    if "fat_unit" in item["nutriments"]:
                        nutri_val.fat_unit = item["nutriments"]["fat_unit"]
                    if "saturated-fat_serving" in item["nutriments"]:
                        nutri_val.saturatedFat = \
                            item["nutriments"]["saturated-fat_serving"]
                    if "saturated-fat_100g" in item["nutriments"]:
                        nutri_val.saturatedFat_per100 = \
                            item["nutriments"]["saturated-fat_100g"]
                    if "saturated-fat_unit" in item["nutriments"]:
                        nutri_val.saturatedFat_unit = \
                            item["nutriments"]["saturated-fat_unit"]
                    if "carbohydrates_serving" in item["nutriments"]:
                        nutri_val.carbohydrates = \
                            item["nutriments"]["carbohydrates_serving"]
                    if "carbohydrates_100g" in item["nutriments"]:
                        nutri_val.carbohydrates_per100 = \
                            item["nutriments"]["carbohydrates_100g"]
                    if "carbohydrates_unit" in item["nutriments"]:
                        nutri_val.carbohydrates_unit = \
                            item["nutriments"]["carbohydrates_unit"]
                    if "sugars_serving" in item["nutriments"]:
                        nutri_val.sugar = item["nutriments"]["sugars_serving"]
                    if "sugars_100g" in item["nutriments"]:
                        nutri_val.sugar_per100 = item["nutriments"]["sugars_100g"]
                    if "sugars_unit" in item["nutriments"]:
                        nutri_val.sugar_unit = item["nutriments"]["sugars_unit"]
                    if "fiber_serving" in item["nutriments"]:
                        nutri_val.fiber = item["nutriments"]["fiber_serving"]
                    if "fiber_100g" in item["nutriments"]:
                        nutri_val.fiber_per100 = item["nutriments"]["fiber_100g"]
                    if "fiber_unit" in item["nutriments"]:
                        nutri_val.fiber_unit = item["nutriments"]["fiber_unit"]
                    if "proteins_serving" in item["nutriments"]:
                        nutri_val.proteins = item["nutriments"]["proteins_serving"]
                    if "proteins_100g" in item["nutriments"]:
                        nutri_val.proteins_per100 = \
                            item["nutriments"]["proteins_100g"]
                    if "proteins_unit" in item["nutriments"]:
                        nutri_val.proteins_unit = \
                            item["nutriments"]["proteins_unit"]
                    if "salt_serving" in item["nutriments"]:
                        nutri_val.salt = item["nutriments"]["salt_serving"]
                    if "salt_100g" in item["nutriments"]:
                        nutri_val.salt_per100 = item["nutriments"]["salt_100g"]
                    if "salt_unit" in item["nutriments"]:
                        nutri_val.salt_unit = item["nutriments"]["salt_unit"]
            logger.info(f"Product {product.name} successfully updated")
        logger.info("Product database successfully updated")
