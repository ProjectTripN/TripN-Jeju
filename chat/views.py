from django.shortcuts import render

# Create your views here.

import json
from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes

from chat.model_data import ChatDbUploader
from chat.model_process import ChatProcess, Chat
from chat.test.test_train_model import TestChat


@api_view(['GET'])
@parser_classes([JSONParser])
def uploaderDB(request):
    print('############ 1 ##########')
    ChatDbUploader().insert_data()
    return JsonResponse({'Product Upload': 'SUCCESS'})

@api_view(['POST'])
@parser_classes([JSONParser])
def with_who(request):
    print('############ 1 ##########')
    print(f'hi : {request}')
    print(f'hello : {request.data}')
    with_test = {"with" : Chat().test_with(request.data['sentence'])}
    print('############ 2 ##########')
    print(with_test)
    return JsonResponse(data=with_test, safe=False)

@api_view(['POST'])
@parser_classes([JSONParser])
def where_air(request):
    print('############ 1 ##########')
    where_test = Chat().test_air(request)
    print('############ 2 ##########')
    return JsonResponse(data=where_test, safe=False)


@api_view(['POST'])
@parser_classes([JSONParser])
def chat(request):
    print('############ 1 ##########')
    print(request.data)
    a = request.data['value']
    print(a)
    print('############ 2 ##########')
    predict = TestChat().predict_test(a)
    print('############ 3 ##########')
    try:
        cp = ChatProcess()
        if predict[0] <= 106:  # F&A
            answer = cp.q_answer(predict)
            # return JsonResponse({'Product chat': f'{answer}'})
        elif 107 <= predict[0] <= 112:  # weather
            answer = cp.w_answer(predict)
            # return JsonResponse({'Product chat': f'{answer}'})
        elif 113 <= predict[0] <= 120:  # tourism
            answer = cp.tourism_answer(predict)
            # return JsonResponse({'Product chat': f'{answer}'})
        elif 121 <= predict[0] <= 144:  # activity
            answer = cp.activity_answer(predict)
            # return JsonResponse({'Product chat': f'{answer}'})
        elif 145 <= predict[0] <= 160:  # restaurant
            answer = cp.restaurant_answer(predict)
            # return JsonResponse({'Product chat': f'{answer}'})
        elif 161 <= predict[0] <= 162:  # shop
            answer = cp.shop_answer(predict)
            # return JsonResponse({'Product chat': f'{answer}'})

        answer = {"chat": answer}
        print('############ 4 try ##########')

    except:
        answer = {"chat": "다시 한번 말씀해 주세요"}
        print('############ 4 except ##########')

    answer['queryid'] = request.data['key']
    print('############ 끝 ##########')

    return JsonResponse(data=answer, safe=False)