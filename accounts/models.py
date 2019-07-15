from django.db import models
from django.contrib.auth.models import AbstractUser

from search.models import Products


class MyUser(AbstractUser):

    avatar = models.ImageField(blank=True)
    favorites = models.ManyToManyField(Products,
                                       related_name='favorites')

    REQUIRED_FIELDS = ['first_name', 'email']

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name
