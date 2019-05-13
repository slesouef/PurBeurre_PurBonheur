from django.db import models

from accounts.models import MyUser


class Categories(models.Model):
    name = models.CharField(max_length=254)


class Products(models.Model):
    name = models.CharField(max_length=254)
    brand = models.CharField(max_length=254)
    quantity = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    rating = models.CharField(max_length=1)
    url = models.URLField()
    image = models.URLField(null=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    favorites = models.ManyToManyField(MyUser,
                                       related_name='favorites')


class NutritionalValues(models.Model):
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
    pid = models.OneToOneField('Products', on_delete=models.CASCADE)
