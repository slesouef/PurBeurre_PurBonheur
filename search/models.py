"""
App specific database models for the product information from OpenFoodFacts
"""
from django.db import models


class Categories(models.Model):
    """All products must have one category. A category has a name"""
    name = models.CharField(max_length=254)


class Products(models.Model):
    """
    All products must have the following fields:
        a name, a brand, a quantity, a rating, an url, and a category
    A product can also contain:
        a description and an image
    """
    name = models.CharField(max_length=254)
    brand = models.CharField(max_length=254)
    quantity = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    rating = models.CharField(max_length=1)
    url = models.URLField()
    image = models.URLField(null=True)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)

    def get_absolute_url(self):
        """
        Method used to create a url for a specific product identified
        by id
        """
        from django.urls import reverse
        return reverse("details", args=[int(self.id)])


class NutritionalValues(models.Model):
    """
    The nutritional values of a product are all optional fields
    A set of nutritional values can only be associated with a single Product
    """
    serving_size = models.CharField(max_length=254, blank=True)
    energy = models.CharField(max_length=254, blank=True)
    energy_per100 = models.CharField(max_length=254, blank=True)
    energy_unit = models.CharField(max_length=254, blank=True)
    fat = models.CharField(max_length=254, blank=True)
    fat_per100 = models.CharField(max_length=254, blank=True)
    fat_unit = models.CharField(max_length=254, blank=True)
    saturatedFat = models.CharField(max_length=254, blank=True)
    saturatedFat_per100 = models.CharField(max_length=254, blank=True)
    saturatedFat_unit = models.CharField(max_length=254, blank=True)
    carbohydrates = models.CharField(max_length=254, blank=True)
    carbohydrates_per100 = models.CharField(max_length=254, blank=True)
    carbohydrates_unit = models.CharField(max_length=254, blank=True)
    sugar = models.CharField(max_length=254, blank=True)
    sugar_per100 = models.CharField(max_length=254, blank=True)
    sugar_unit = models.CharField(max_length=254, blank=True)
    fiber = models.CharField(max_length=254, blank=True)
    fiber_per100 = models.CharField(max_length=254, blank=True)
    fiber_unit = models.CharField(max_length=254, blank=True)
    proteins = models.CharField(max_length=254, blank=True)
    proteins_per100 = models.CharField(max_length=254, blank=True)
    proteins_unit = models.CharField(max_length=254, blank=True)
    salt = models.CharField(max_length=254, blank=True)
    salt_per100 = models.CharField(max_length=254, blank=True)
    salt_unit = models.CharField(max_length=254, blank=True)
    pid = models.OneToOneField("Products", on_delete=models.CASCADE)
