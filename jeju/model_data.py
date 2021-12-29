import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

import django
django.setup()
import datetime

from jeju.models import JejuScheduleDetail


class DbUploader():


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

if __name__ == '__main__':
    DbUploader().updata_jeju_dday()