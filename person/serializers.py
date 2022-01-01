from rest_framework import serializers
# pip install Django django-rest-framework
# from .models import User as person
#
# class UserSerializer(serializers.Serializer):
#
#     id = serializers.IntegerField()
#     username = serializers.CharField()
#     password = serializers.CharField()
#     name = serializers.CharField()
#     email = serializers.EmailField()
#     birth = serializers.DateField()
#     gender = serializers.BooleanField()
#     mbti = serializers.CharField()
#     mbti_list = serializers.CharField()
#     card_number = serializers.IntegerField()
#     card_company = serializers.CharField()
#     regDate = serializers.DateField()
#
#     class Meta:
#         model = person
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return person.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         person.objects.filter(pk=instance.id).update(**validated_data)