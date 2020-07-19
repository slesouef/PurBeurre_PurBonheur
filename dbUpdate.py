import openfoodfacts

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

Base = automap_base()

eng = create_engine("postgresql://sebastien:sebastien@localhost/offproducts")

Base.prepare(eng, reflect=True)

Products = Base.classes.search_products
Nutrition_values = Base.classes.search_nutritionalvalues

sesh = Session(eng)

for product in sesh.query(Products):
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
            for nutriVal in sesh.query(Nutrition_values) \
                                .filter(Nutrition_values.pid_id == product.id):
                if "serving_size" in item:
                    nutriVal.serving_size = item["serving_size"]
                if "energy_serving" in item["nutriments"]:
                    nutriVal.energy = item["nutriments"]["energy_serving"]
                if "energy_100g" in item["nutriments"]:
                    nutriVal.energy_per100 = item["nutriments"]["energy_100g"]
                if "energy_unit" in item["nutriments"]:
                    nutriVal.energy_unit = item["nutriments"]["energy_unit"]
                if "fat_serving" in item["nutriments"]:
                    nutriVal.fat = item["nutriments"]["fat_serving"]
                if "fat_100g" in item["nutriments"]:
                    nutriVal.fat_per100 = item["nutriments"]["fat_100g"]
                if "fat_unit" in item["nutriments"]:
                    nutriVal.fat_unit = item["nutriments"]["fat_unit"]
                if "saturated-fat_serving" in item["nutriments"]:
                    nutriVal.saturatedFat = \
                        item["nutriments"]["saturated-fat_serving"]
                if "saturated-fat_100g" in item["nutriments"]:
                    nutriVal.saturatedFat_per100 = \
                        item["nutriments"]["saturated-fat_100g"]
                if "saturated-fat_unit" in item["nutriments"]:
                    nutriVal.saturatedFat_unit = \
                        item["nutriments"]["saturated-fat_unit"]
                if "carbohydrates_serving" in item["nutriments"]:
                    nutriVal.carbohydrates = \
                        item["nutriments"]["carbohydrates_serving"]
                if "carbohydrates_100g" in item["nutriments"]:
                    nutriVal.carbohydrates_per100 = \
                        item["nutriments"]["carbohydrates_100g"]
                if "carbohydrates_unit" in item["nutriments"]:
                    nutriVal.carbohydrates_unit = \
                        item["nutriments"]["carbohydrates_unit"]
                if "sugars_serving" in item["nutriments"]:
                    nutriVal.sugar = item["nutriments"]["sugars_serving"]
                if "sugars_100g" in item["nutriments"]:
                    nutriVal.sugar_per100 = item["nutriments"]["sugars_100g"]
                if "sugars_unit" in item["nutriments"]:
                    nutriVal.sugar_unit = item["nutriments"]["sugars_unit"]
                if "fiber_serving" in item["nutriments"]:
                    nutriVal.fiber = item["nutriments"]["fiber_serving"]
                if "fiber_100g" in item["nutriments"]:
                    nutriVal.fiber_per100 = item["nutriments"]["fiber_100g"]
                if "fiber_unit" in item["nutriments"]:
                    nutriVal.fiber_unit = item["nutriments"]["fiber_unit"]
                if "proteins_serving" in item["nutriments"]:
                    nutriVal.proteins = item["nutriments"]["proteins_serving"]
                if "proteins_100g" in item["nutriments"]:
                    nutriVal.proteins_per100 = \
                        item["nutriments"]["proteins_100g"]
                if "proteins_unit" in item["nutriments"]:
                    nutriVal.proteins_unit = \
                        item["nutriments"]["proteins_unit"]
                if "salt_serving" in item["nutriments"]:
                    nutriVal.salt = item["nutriments"]["salt_serving"]
                if "salt_100g" in item["nutriments"]:
                    nutriVal.salt_per100 = item["nutriments"]["salt_100g"]
                if "salt_unit" in item["nutriments"]:
                    nutriVal.salt_unit = item["nutriments"]["salt_unit"]
                sesh.commit()
