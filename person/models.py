import os
import django

from django.db import models

# Create your models here.
from image.models import Category, Image
from django_mysql.models import ListCharField
from django.db.models import IntegerField


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

# class Pay(models.Model):
#
#     re_id = models.IntegerField(primary_key=True)
#     reg_date = models.DateField()
#     user = models.IntegerField()
#     day = models.IntegerField()
#     people = models.IntegerField()
#     plane = ListCharField(base_field=IntegerField(), size=50, null=True, max_length=100)
#     acc = models.IntegerField()
#     activity = ListCharField(base_field=IntegerField(), size=50, null=True, max_length=100)
#     class Meta:
#         db_table = "pay"
#
#     def __str__(self):
#         return f'[{self.pk}]'
