import os
import django

from django.db import models

# Create your models here.
from image.models import Category, Image



class Person(models.Model):

    # use_in_migrations = True
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    age = models.IntegerField()
    gender = models.BooleanField()
    mbti = models.TextField()


    class Meta:
        db_table = "person"

    def __str__(self):
        return f'[{self.pk}]'

