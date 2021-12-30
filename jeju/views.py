import random

import datetime
from django.shortcuts import render
from django.http import JsonResponse
from icecream import ic
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes
import csv

# Create your views here.
from image.models import Category
from jeju.model_data import DbUploader
from jeju.models import JejuScheduleDetail
from jeju.models_process import JejuProcess
from jeju.serializer import JejuDSerializer
from jeju_data.models import Plane, PlaneCategory, Accommodation, Activity
from jeju_data.serializer import PlaneSerializer, AccommodationSerializer
# from user.models import User

@api_view(['POST'])
@parser_classes([JSONParser])
def recommendation(request):
    jeju = JejuProcess(request.data)
    mbti = jeju.mbti_set()
    day = {"day": jeju.count_day()}
    plane = jeju.plane()
    departure_plane = plane[0].data
    arrival_plane = plane[1].data
    accommodation = jeju.accommodation(mbti).data
    activity = jeju.activity(mbti).data
    # if jeju.olle() == 0:
    #     return JsonResponse(data=(departure_plane, arrival_plane, accommodation, day, activity), safe=False)
    # else:
    #     if jeju.olle()[0] == None :
    #         oleum = jeju.olle()[1]
    #         return JsonResponse(data=(departure_plane, arrival_plane, accommodation, day, activity, oleum), safe=False)
    #     if jeju.olle()[1] == None :
    #         olle = jeju.olle()[0]
    #         return JsonResponse(data=(departure_plane, arrival_plane, accommodation, day, activity, olle), safe=False)
    #     else:
    #         oleum = jeju.olle()[1]
    #         olle = jeju.olle()[0]
    #         return JsonResponse(data=(departure_plane, arrival_plane, accommodation, day, activity, olle, oleum), safe=False)
    if jeju.olle() == 0:
        return JsonResponse(data=(day, departure_plane, arrival_plane, accommodation, activity), safe=False)
    else:
        if jeju.olle()[0] == None :
            oleum = jeju.olle()[1].data
            return JsonResponse(data=(day, departure_plane, arrival_plane, accommodation, activity, oleum), safe=False)
        if jeju.olle()[1] == None :
            olle = jeju.olle()[0].data
            return JsonResponse(data=(day, departure_plane, arrival_plane, accommodation, activity, olle), safe=False)
        else:
            oleum = jeju.olle()[1].data
            olle = [jeju.olle()[0].data, jeju.olle()[1].data]
            return JsonResponse(data=(day, departure_plane, arrival_plane, accommodation, activity, olle), safe=False)


@api_view(['POST'])
@parser_classes([JSONParser])
def days(request):
    check = request.data
    jeju = JejuProcess(request.data)
    days = jeju.process_days(request.data)
    activity = {"activity" : [Activity.objects.filter(id__in=request.data['activty']).values()[0]['name'], Activity.objects.filter(id__in=request.data['activty']).values()[1]['name']]}
    print(activity)
    plane_data = Plane.objects.filter(id__in=days[1]).values()
    plane_data = PlaneSerializer(plane_data, many=True).data
    plane = {"plane" : plane_data}
    acc_data = Accommodation.objects.filter(id=days[2]).values()
    acc_data = AccommodationSerializer(acc_data, many=True).data
    acc = {"acc": acc_data}

    return JsonResponse(data=(plane, acc, activity, days[0]), safe=False)





@api_view(['PUT'])
@parser_classes([JSONParser])
def down(request):
    with open('jeju/data/jeju_schedule_detail.csv', 'w', newline='', encoding='utf8') as csvfile:
        fieldnames = ['id', 'user', 'startday', 'endday', 'day', 'reg_date', 'startloc', 'people', 'relationship',
                      'category', 'plane',
                      'plane_detail', 'acc', 'acc_detail', 'activity', 'activity_name', 'olle', 'restaurant', 'tourism',
                      'shop', 'dday', 'schedule']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # schedule = JejuScheduleDetail.objects.all()
        # jds = JejuDSerializer(schedule).data

        for schedule in JejuScheduleDetail.objects.all():
            writer.writerow(
                {'id': schedule.id, 'user': schedule.user, 'startday': schedule.startday, 'endday': schedule.endday,
                 'day': schedule.day, 'reg_date': schedule.reg_date,
                 'startloc': schedule.startloc, 'people': schedule.people, 'relationship': schedule.relationship,
                 'category': schedule.category, 'plane': schedule.plane,
                 'plane_detail': schedule.plane_detail, 'acc': schedule.acc, 'acc_detail': schedule.acc_detail,
                 'activity': schedule.activity, 'activity_name': schedule.activity_name,
                 'olle': schedule.olle, 'restaurant': schedule.restaurant, 'tourism': schedule.tourism,
                 'shop': schedule.shop, 'dday': schedule.dday, 'schedule': schedule.schedule})

    print('Schedule DATA DOWNLOADED SUCCESSFULY!')
    return JsonResponse({"DbUploader:down": "!!SUCCESSFULY!!"})



# @api_view(['POST'])
# @parser_classes([JSONParser])
# def days_d(request):
#     check = request.data
#     jeju = JejuProcess(request.data)
#     days = jeju.process_days(request.data)
#     activity = [Activity.objects.filter(id__in=request.data['activty']).values()[0]['name'], Activity.objects.filter(id__in=request.data['activty']).values()[1]['name']]
#     print(activity)
#     plane_data = Plane.objects.filter(id__in=days[1]).values()
#     plane_data = PlaneSerializer(plane_data, many=True).data
#     plane = {"plane" : plane_data}
#     acc_data = Accommodation.objects.filter(id=days[2]).values()
#     acc_data = AccommodationSerializer(acc_data, many=True).data
#     acc = {"acc": acc_data}
#     # count = JejuScheduleDetail.objects.all()
#     # c = Category()
#     # category = Category.objects.all().filter(category='recommend').values()[0]
#     # c.id = category['id']
#     # ac = Accommodation()
#     # accommodation = Accommodation.objects.filter(id=check['acc']).values()[0]
#     # ac.id = accommodation['id']
#     # jeju_detail = JejuScheduleDetail.objects.create(
#     #     user=check['user'], id=count.count()+1, startday=datetime.datetime.strptime(check['date1'], '%Y-%m-%d'), endday=datetime.datetime.strptime(check['date2'], '%Y-%m-%d'),
#     #     day=jeju.count_day(), reg_date=(datetime.strptime(check['date1'], '%Y-%m-%d'))-random.randrange(30), startloc=check['start'], people=check['Number'], relationship=check['relationship'],
#     #     category=c, plane=check['plane'], plane_detail=plane_data, acc=ac, acc_detail=acc_data, activity=check['activty'], activity_name=activity, olle=check['olle'],restaurant
#     # )
#     return JsonResponse(data=(plane, acc, activity, days[0]), safe=False)



@api_view(['POST'])
@parser_classes([JSONParser])
def save_days(request):
    check = request.data
    jeju = JejuProcess(request.data)
    days = jeju.process_save_days(request.data)
    plane_data = Plane.objects.filter(id__in=days[1]).values()
    plane_data = PlaneSerializer(plane_data, many=True).data
    acc_data = Accommodation.objects.filter(id=check['acc']).values()
    acc_data = AccommodationSerializer(acc_data, many=True).data

    activity = [Activity.objects.filter(id__in=days[2]).values()[0]['name'],
                             Activity.objects.filter(id__in=days[2]).values()[1]['name']]
    print(activity)
    count = JejuScheduleDetail.objects.all()
    c = Category()
    category = Category.objects.all().filter(category='recommend').values()[0]
    c.id = category['id']
    ac = Accommodation()
    accommodation = Accommodation.objects.filter(id=check['acc']).values()[0]
    ac.id = accommodation['id']
    dday = datetime.datetime.strptime(check['date1'], '%Y-%m-%d') - datetime.datetime.today()
    jeju_detail = JejuScheduleDetail.objects.create(
        user=check['user'], id=count.count()+3, startday=datetime.datetime.strptime(check['date1'], '%Y-%m-%d'),
        endday=datetime.datetime.strptime(check['date2'], '%Y-%m-%d'),
        day=jeju.count_day(), reg_date=(datetime.datetime.strptime(check['date1'], '%Y-%m-%d'))-datetime.timedelta(days=random.randrange(20)),
        startloc=check['start'], people=check['Number'], relationship=check['relationship'],
        category=c, plane=check['plane'], plane_detail=plane_data, acc=ac, acc_detail=acc_data,
        activity=check['activty'], activity_name=activity, olle=check['olle'], restaurant=days[3], tourism=days[4], shop=days[5], dday=dday, schedule=days[0]
    )

    jds = JejuDSerializer(jeju_detail).data
    return JsonResponse(data=(jds), safe=False)
    # if len(days) == 13:
    #     js_data = JejuSchedule.objects.filter(user=days[11]['user'], startday=days[7]['startday'], endday=days[8]['endday']).values()
    #     js = JejuSerializer(js_data, many=True).data
    #     return JsonResponse(data=(jds),safe=False)
    #
    # if len(days) == 14:
    #     olle = {"olle" : days[13]}
    #     js_data = JejuSchedule.objects.filter(user=days[11]['user'], startday=days[7]['startday'], endday=days[8]['endday']).values()
    #     js = JejuSerializer(js_data, many=True).data
    #     return JsonResponse(data=(jds), safe=False)
#
# @api_view(['POST'])
# @parser_classes([JSONParser])
# def save_days_d(request):
#     jeju = JejuProcess(request.data)
#     days = jeju.process_save_days(request.data)
#     plane_data = Plane.objects.filter(id__in=days[1]).values()
#     plane_data = PlaneSerializer(plane_data, many=True).data
#     plane = {"plane": plane_data}
#     acc_data = Accommodation.objects.filter(id=days[2]).values()
#     acc_data = AccommodationSerializer(acc_data, many=True).data
#     acc = {"acc": acc_data}  # acc
#     # activity = {"activity" : days[3]}
#     activity = {"activity": [Activity.objects.filter(id__in=days[3]).values()[0]['name'],
#                              Activity.objects.filter(id__in=days[3]).values()[1]['name']]}
#     print(activity)
#     restaurant = {"restaurant" : days[4]}
#     tourism = {"tourism" : days[5]}
#     shop = {"shop" : days[6]}
#     startday = days[7]
#     endday = days[8]
#     day = days[9]
#     people = days[10]
#     user = days[11]
#     relationship = days[12]
#     print(days[11], days[7], days[8])
#     if len(days) == 13:
#         js_data = JejuSchedule.objects.filter(user=days[11]['user'], startday=days[7]['startday'], endday=days[8]['endday']).values()
#         js = JejuSerializer(js_data, many=True).data
#         return JsonResponse(data=(js, days[0], plane, acc, activity, restaurant, tourism, shop, startday, endday, day, people, user, relationship),safe=False)
#
#     if len(days) == 14:
#         olle = {"olle" : days[13]}
#         js_data = JejuSchedule.objects.filter(user=days[11]['user'], startday=days[7]['startday'], endday=days[8]['endday']).values()
#         js = JejuSerializer(js_data, many=True).data
#         return JsonResponse(data=(js, days[0], plane, acc, activity, olle, restaurant, tourism, shop, startday, endday, day, people, user, relationship), safe=False)

# @api_view(['GET', 'POST'])
# @parser_classes([JSONParser])
# def list_by_user(request, user_id):
#     jejuSchedule = JejuScheduleDetail.objects.all()
#     serializer = JejuDSerializer(jejuSchedule, many=True)
#     return JsonResponse(data = serializer.data, safe=False)

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_by_user_d(request, user):
    jejuSchedule = JejuScheduleDetail.objects.filter(user=user).values()
    serializer = JejuDSerializer(jejuSchedule, many=True)
    return JsonResponse(data=serializer.data, safe=False)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_all(request):
    jejuSchedule = JejuScheduleDetail.objects.all()
    serializer = JejuDSerializer(jejuSchedule, many=True)
    return JsonResponse(data = serializer.data, safe=False)



@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_by_user_pr(request, user):

    today = datetime.date.today()
    jejuSchedule = JejuScheduleDetail.objects.raw(
        f"select * from jeju_schedule_detail where user_id = {user} and startday > '{today}';")
    serializer = JejuDSerializer(jejuSchedule, many=True)

    return JsonResponse(data=serializer.data, safe=False)

@api_view(['DELETE'])
@parser_classes([JSONParser])
def del_list_by_user(request, pk):
    print("********** remove **********")
    print(f'pk : {pk}')
    jejuSchedule = JejuScheduleDetail.objects.get(pk=pk)
    jejuSchedule.delete()

    return JsonResponse({'User want JejuSchedule': 'DELETE SUCCESS'})

@api_view(['PUT'])
@parser_classes([JSONParser])
def dday_up(request):
    DbUploader().updata_jeju_dday()
    return JsonResponse({"JEJU_dday DATA UPLOADED": "SUCCESSFULY!"})

