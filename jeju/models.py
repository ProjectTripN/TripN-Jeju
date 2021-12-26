from datetime import datetime
from random import random

from django.db import models

# Create your models here.
from icecream import ic

from django.db.models import IntegerField, CharField
from django_mysql.models import ListCharField, ListTextField
from image.models import Category
from jeju_data.models import Accommodation
from user.models import User


class JejuSchedule(models.Model):

    # days[0], plane, acc, activity, olle, restaurant, tourism, shop, startday, endday, day, people, user, relationship
    # Jeju_Schedule

    user = models.IntegerField()  # user
    reg_date = models.DateTimeField(default=datetime.now())  # 생성일
    startday = models.DateField()  # startday
    endday = models.DateField()  # endday
    day = models.IntegerField()  # day
    startloc = models.TextField()  # startloc
    people = models.IntegerField()  # people
    relationship = models.TextField()  # relationship
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # recommend
    plane = ListCharField(base_field=IntegerField(), size=5, max_length=100)  # plane
    acc = models.ForeignKey(Accommodation, max_length=255, on_delete=models.CASCADE)  # acc
    activity = ListCharField(base_field=IntegerField(), size=50, null=True, max_length=100)  # activity
    olle = ListCharField(base_field=IntegerField(), size=50, null=True, max_length=100)  # olle
    restaurant = ListCharField(base_field=IntegerField(), size=100, null=True, max_length=100)  # restaurant
    tourism = ListCharField(base_field=IntegerField(), size=100, null=True, max_length=100)  # tourism
    shop = ListCharField(base_field=IntegerField(), size=50, null=True, max_length=100)  # shop
    schedule = ListTextField(base_field=CharField(max_length=255), size=50, null=True)  # days[0]
    dday = models.TextField()

    class Meta:
        db_table = "jeju_schedule"

    def __str__(self):
        return f'{self.id}'