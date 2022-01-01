import os

from image.models import Category
from jeju.serializer import JejuDSerializer
from jeju_data.models import Accommodation

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

import django
django.setup()
import csv
import datetime
from common.models import ValueObject, Reader, Printer

from jeju.models import JejuScheduleDetail
import json


class DbUploader():

    def __init__(self):
        vo = ValueObject()
        reader = Reader()
        self.printer = Printer()
        vo.context = 'jeju/data/'
        vo.fname = 'jeju_schedule_detail.csv'
        self.csvfile = reader.new_file(vo)


    def updata_jeju_dday(self):
        today = datetime.date.today()
        print(today)
        j = JejuScheduleDetail.objects.all().values()

        for row in j:
            print(row['id'])
            print(row['dday'])
            jejuSchedule = JejuScheduleDetail.objects.filter(id=row['id']).update(dday=row['startday']-today)
            print(jejuSchedule)
            print("===========================")

        print('JEJU_dday DATA UPLOADED SUCCESSFULY!')

    def insert_schedule(self):
        with open(self.csvfile, newline='', encoding='utf8') as f:
            data_reader = csv.DictReader(f)
            for row in data_reader:
                c = Category()
                category = Category.objects.all().filter(category='recommend').values()[0]
                c.id = category['id']
                ac = Accommodation()
                accommodation = Accommodation.objects.all().filter(category=row['acc_id']).values()[0]
                ac.id = accommodation['id']
                if not JejuScheduleDetail.objects.filter(id=row['id'], user=row['person'], reg_date=row['reg_date']).exists():  # 동일한 값 있으면 넘어가
                    jeju_detail = JejuScheduleDetail.objects.create(user=row['person'], id=row['id'], startday=row['startday'],
                                                                    endday=row['endday'], day=row['day'], reg_date=row['reg_date'],
                                                                    startloc=row['startloc'], people=row['people'], relationship=row['relationship'],
                                                                    category=c, plane=row['plane'], plane_detail=row['plane_detail'],
                                                                    acc=ac, acc_detail=row['acc_detail'], activity=row['activity'],
                                                                    activity_name=row['activity_name'], olle=row['olle'], restaurant=row['restaurant'],
                                                                    tourism=row['tourism'], shop=row['shop'], dday=row['dday'], schedule=row['schedule'])

                    print(f' 1 >>>> {jeju_detail}')
        print('Schedule DATA UPLOADED SUCCESSFULY!')

    def data_set_schedule(self):
        with open('jeju/data/jeju_schedule_detail.csv', 'w', newline='', encoding='utf8') as csvfile:
            fieldnames = ['id', 'person', 'startday', 'endday', 'day', 'reg_date', 'startloc', 'people', 'relationship', 'category', 'plane',
                          'plane_detail', 'acc', 'acc_detail', 'activity', 'activity_name', 'olle', 'restaurant', 'tourism', 'shop', 'dday', 'schedule']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            schedule = JejuScheduleDetail.objects.all()
            jds = JejuDSerializer(schedule).data

            for schedule in jds:
                writer.writerow({'id':schedule.id, 'person':schedule.user, 'startday':schedule.startday, 'endday':schedule.endday, 'day':schedule.day, 'reg_date':schedule.reg_date,
                                 'startloc':schedule.startloc, 'people':schedule.people, 'relationship':schedule.relationship, 'category':schedule.category, 'plane':schedule.plane,
                                 'plane_detail':schedule.plane_detail, 'acc':schedule.acc, 'acc_detail':schedule.acc_detail, 'activity':schedule.activity, 'activity_name':schedule.activity_name,
                                 'olle':schedule.olle, 'restaurant':schedule.restaurant, 'tourism':schedule.tourism, 'shop':schedule.shop, 'dday':schedule.dday, 'schedule':schedule.schedule})

        print('Schedule DATA DOWNLOADED SUCCESSFULY!')

if __name__ == '__main__':
    DbUploader().updata_jeju_dday()

