from rest_framework import serializers
import datetime as dt
from jeju.models import JejuScheduleDetail as jeju


# class JejuSerializer(serializers.Serializer):
#
#
#     id = serializers.CharField()
#     user = serializers.CharField()
#     reg_date = serializers.DateTimeField()
#     startday = serializers.DateField()
#     endday = serializers.DateField()
#     day = serializers.IntegerField()
#     startloc = serializers.CharField()
#     people = serializers.IntegerField()
#     relationship = serializers.CharField()
#     category_id = serializers.CharField()
#     plane = serializers.ListField()
#     acc_id = serializers.CharField()
#     activity = serializers.ListField()
#     olle = serializers.ListField()
#     restaurant = serializers.ListField()
#     tourism = serializers.ListField()
#     shop = serializers.ListField()
#     schedule = serializers.CharField()
#     dday = serializers.DateField()
#
#
#     class Meta:
#         model = jeju
#         fileds = '__all__'
#
#     def create(self, validated_data):
#         return jeju.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         jeju.objects.filter(pk=instance.id).update(**validated_data)

class JejuDSerializer(serializers.Serializer):


    id = serializers.CharField()
    user = serializers.IntegerField()
    reg_date = serializers.CharField()
    startday = serializers.CharField()
    endday = serializers.CharField()
    day = serializers.IntegerField()
    startloc = serializers.CharField()
    people = serializers.IntegerField()
    relationship = serializers.CharField()
    category_id = serializers.IntegerField()
    plane = serializers.ListField()
    plane_detail = serializers.ListField()
    acc_id = serializers.IntegerField()
    acc_detail = serializers.ListField()
    activity = serializers.ListField()
    activity_name = serializers.ListField()
    olle = serializers.ListField()
    restaurant = serializers.ListField()
    tourism = serializers.ListField()
    shop = serializers.ListField()
    schedule = serializers.CharField()
    dday = serializers.JSONField()


    class Meta:
        model = jeju
        fileds = '__all__'

    def create(self, validated_data):
        return jeju.objects.create(**validated_data)

    def update(self, instance, validated_data):
        jeju.objects.filter(pk=instance.id).update(**validated_data)