import random

import datetime
from django.shortcuts import render
from django.http import JsonResponse
from icecream import ic
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes

# Create your views here.
from jeju.model_data import DbUploader
from jeju.models import JejuSchedule
from jeju.models_process import JejuProcess
from jeju.serializer import JejuSerializer
from jeju_data.models import Plane, PlaneCategory, Accommodation
from jeju_data.serializer import PlaneSerializer, AccommodationSerializer
from user.models import User

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
    jeju = JejuProcess(request.data)
    days = jeju.process_days(request.data)
    plane_data = Plane.objects.filter(id__in=days[1]).values()
    plane_data = PlaneSerializer(plane_data, many=True).data
    plane = {"plane" : plane_data}
    acc_data = Accommodation.objects.filter(id=days[2]).values()
    acc_data = AccommodationSerializer(acc_data, many=True).data
    acc = {"acc": acc_data}

    return JsonResponse(data=(plane, acc, days[0]), safe=False)


@api_view(['POST'])
@parser_classes([JSONParser])
def save_days(request):
    jeju = JejuProcess(request.data)
    days = jeju.process_save_days(request.data)
    plane_data = Plane.objects.filter(id__in=days[1]).values()
    plane_data = PlaneSerializer(plane_data, many=True).data
    plane = {"plane": plane_data}
    acc_data = Accommodation.objects.filter(id=days[2]).values()
    acc_data = AccommodationSerializer(acc_data, many=True).data
    acc = {"acc": acc_data}  # acc
    activity = {"activity" : days[3]}
    restaurant = {"restaurant" : days[4]}
    tourism = {"tourism" : days[5]}
    shop = {"shop" : days[6]}
    startday = days[7]
    endday = days[8]
    day = days[9]
    people = days[10]
    user = days[11]
    relationship = days[12]
    print(days[11], days[7], days[8])
    if len(days) == 13:
        js_data = JejuSchedule.objects.filter(user=days[11]['user'], startday=days[7]['startday'], endday=days[8]['endday']).values()
        js = JejuSerializer(js_data, many=True).data
        return JsonResponse(data=(js, days[0], plane, acc, activity, restaurant, tourism, shop, startday, endday, day, people, user, relationship),safe=False)

    if len(days) == 14:
        olle = {"olle" : days[13]}
        js_data = JejuSchedule.objects.filter(user=days[11]['user'], startday=days[7]['startday'], endday=days[8]['endday']).values()
        js = JejuSerializer(js_data, many=True).data
        return JsonResponse(data=(js, days[0], plane, acc, activity, olle, restaurant, tourism, shop, startday, endday, day, people, user, relationship), safe=False)

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_by_user(request, user_id):
    jejuSchedule = JejuSchedule.objects.all()
    serializer = JejuSerializer(jejuSchedule, many=True)
    return JsonResponse(data = serializer.data, safe=False)

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_all(request):
    jejuSchedule = JejuSchedule.objects.filter()
    serializer = JejuSerializer(jejuSchedule, many=True)
    return JsonResponse(data = serializer.data, safe=False)



@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_by_user_pr(request, user_id):

    today = datetime.date.today()
    jejuSchedule = JejuSchedule.objects.raw(
        f"select * from jeju_schedule where user_id = {user_id} and startday > '{today}';")
    serializer = JejuSerializer(jejuSchedule, many=True)

    return JsonResponse(data=serializer.data, safe=False)

@api_view(['DELETE'])
@parser_classes([JSONParser])
def del_list_by_user(request, pk):
    print("********** remove **********")
    print(f'pk : {pk}')
    jejuSchedule = JejuSchedule.objects.get(pk=pk)
    jejuSchedule.delete()

    return JsonResponse({'User want JejuSchedule': 'DELETE SUCCESS'})

@api_view(['PUT'])
@parser_classes([JSONParser])
def dday_up(request):
    DbUploader().updata_jeju_dday()
    return JsonResponse({"JEJU_dday DATA UPLOADED": "SUCCESSFULY!"})

