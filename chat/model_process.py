import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

import django
django.setup()

from chat.data.weather import Weather
from chat.models import Chatbot

import datetime as dt

from jeju_data.models import Tourism, Activity, ActivityCategory, Restaurant, RestaurantCategory, Shop
import re

class ChatProcess:

    def __init__(self):
        pass

    def q_answer(self, intent):
        answer = Chatbot.objects.filter(intentNumber=intent[0]).values('answer').order_by('?').first()
        return answer['answer']

    # 112: '특정 요일 서귀포 날씨', 111: '서귀포 특정 월일 날씨', 110: '서귀포 특정일 날씨', 109: ['서귀포', 53, 33, '모레', ttom], 108: ['서귀포', 53, 33, '내일', tom], 107: ['서귀포', 53, 33, '오늘', today], 106: '특정 요일 제주 날씨',
    #                      105: '제주 특정 월일 날씨', 104: '제주 특정일 날씨', 103: ['제주', 53, 38, '모레', ttom], 102: ['제주', 53, 38, '내일', tom], 101: ['제주', 53, 38, '오늘', today]
    def w_answer(self, intent):
        # 101: ['제주', 53, 38, '오늘', today]
        try:
            w = Weather().weather_pre(intent[1][1], intent[1][2])
            return f'{intent[1][3]} {intent[1][0]}의 평균기온은 {w[(intent[1][4])][1]}도이며, 날씨는 {w[(intent[1][4])][0]} 입니다.'
        except:
            return '기상청에서 해당 날씨를 알 수 없습니다.'
        # print(intent[1][4])
        # if intent[0] <= 106:
        #     # 제주시 위경도
        #     nx = 53
        #     ny = 38
        #     w = Weather().weather_pre(intent[1][1], intent[1][2])
        #     if intent[0] == 101:
        #         # 제주 오늘 날씨
        #         return f"{intent[1][3]} {intent[1][0]}의 평균기온은 {w[(intent[1][4])][1]}도이며, 날씨는 {w[(intent[1][4])][0]} 입니다."
        #     elif intent[0] == 102:
        #         # 제주 내일 날씨
        #         return f'내일 제주의 평균기온 {w[tom][1]}도로, {w[tom][0]} 입니다.'
        #     elif intent[0] == 103:
        #         # 2일 뒤 제주 날씨
        #         return f'모레 제주의 평균기온 {w[ttom][1]}도로, {w[ttom][0]} 입니다.'
        #     else:
        #         return '알 수 없습니다.'
        # else:
        #     # 서귀포시 위경도
        #     nx = 52
        #     ny = 33
        #     w = Weather().weather_pre(nx, ny)
        #     if intent[0] == 107:
        #         # 서귀포 오늘 날씨
        #         return f'오늘 서귀포시는 평균기온 {w[today][1]}도로, {w[today]} 입니다.'
        #     elif intent[0] == 108:
        #         # 서귀포 내일 날씨
        #         return f'내일 서귀포시의 평균기온 {w[tom][1]}도로, {w[tom]} 입니다.'
        #     elif intent[0] == 109:
        #         # 2일 뒤 서귀포 날씨
        #         return f'모레 서귀포시의 평균기온 {w[ttom][1]}도로, {w[ttom]} 입니다.'
        #     else:
        #         return '알 수 없습니다.'


    # 120: {"tour_category_id": 12, "address__contains": '서귀포'}, 119: {"tour_category_id__in": [1], "address__contains": '서귀포'},
    # 118: {"tour_category_id__in": [1, 12], "address__contains": '서귀포'},  117: {"address__contains" : '제주시'},
    # 116: {"tour_category_id": 12, "address__contains": '제주시'}, 115: {"tour_category_id__in": [1], "address__contains": '제주시'},
    # 114: {"tour_category_id__in": [1, 12], "address__contains": '제주시'}, 113: {"address__contains" : '제주시'},

    def tourism_find(self, intent):
        for i in intent[1]:
            if i == 'address__contains':
                answer = Tourism.objects.filter(address__contains=intent[1]['address__contains']).values().order_by('?').first()
                return answer
            elif i == 'tour_category_id__in' and 'address__contains':
                answer = Tourism.objects.filter(address__contains=intent[1]['address__contains'], tour_category_id__in= intent[1]['tour_category_id__in']).values().order_by('?').first()
                return answer
            elif i == 'tour_category_id' and 'address__contains':
                answer = Tourism.objects.filter(address__contains=intent[1]['address__contains'],
                                                tour_category_id=intent[1]['tour_category_id']).values().order_by('?').first()
                return answer
            else:
                answer = None
                return answer

    def tourism_answer(self, intent):
        # 제주 : 113 - 116
        # 전체, 오름, 해수욕장, 그외 명소
        # 서귀포 : 117 - 120
        answer = self.tourism_find(intent)
        if answer != None:
            return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        else:
            return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'

        # if 113 <= intent[0] <= 116 :
        #     tourism = Tourism.objects.filter(address__contains='제주시')
        #     # answer = Chatbot.objects.filter(label=label).values('answer').order_by('?').first()
        #     if intent[0] == 113:  # 제주 전체
        #         answer = tourism.values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #     if intent[0] == 114:  # 제주 명소
        #         answer = tourism.exclude(tour_category_id__in=[1, 12]).values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #     elif intent[0] == 115:  # 제주 해수욕장
        #         answer = tourism.filter(tour_category_id__in=[1]).values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #     elif intent[0] == 116:  # 제주 오름
        #         answer = tourism.filter(tour_category_id=12).values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #
        #     else:
        #         return '알 수 없습니다.'
        # elif 117 <= intent[0] <= 120:
        #     tourism = Tourism.objects.filter(address__contains='서귀포')
        #     if intent[0] == 117:  # 서귀포 전체
        #         answer = tourism.values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. <br/> 위치는<br/> {answer['address']} 입니다. <br/> {answer['name']}은 <br/> {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #     elif intent[0] == 118:  # 서귀포 명소
        #         answer = tourism.exclude(tour_category_id__in=[1, 12]).values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #     elif intent[0] == 119:  # 서귀포 해수욕장
        #         answer = tourism.filter(tour_category_id=1).values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #     elif intent[0] == 120:  # 서귀포 오름
        #         answer = tourism.filter(tour_category_id=12).values().order_by('?').first()
        #         if answer != None:
        #             return f"{answer['name']}을 추천합니다. \n 위치는\n {answer['address']} 입니다. \n {answer['name']}은 \n {answer['explanation']}"
        #         else:
        #             return '가지고 있는 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        #     else:
        #         return '알 수 없습니다.'

    # 144: {"act_category__type": '요가', "loc__contains": '서귀포'}, 143: {"act_category__type": '요리', "loc__contains": '서귀포'},
    # 142: {"act_category__type": '공예', "loc__contains": '서귀포'}, 141: {"act_category__category": '클래스', "loc__contains": '서귀포'},
    # 140: {"act_category__category": '체험', "loc__contains": '서귀포'}, 139: {"act_category__type": '익스트림액티비티', "loc__contains": '서귀포'},
    # 138: {"act_category__type": '승마', "loc__contains": '서귀포'}, 137: {"act_category__type": '수상액티비티', "loc__contains": '서귀포'}, 136: {"act_category__type": '서핑', "loc__contains": '서귀포'},
    # 135: {"act_category__type": '레이싱', "loc__contains": '서귀포'}, 134: {"act_category__category": '액티비티', "loc__contains": '서귀포'}, 133: {"loc__contains": '서귀포'},

    # 132: {"act_category__type": '요가', "loc__contains": '제주시'}, 131: {"act_category__type": '요리', "loc__contains": '제주시'}, 130: {"act_category__type": '공예', "loc__contains": '제주시'},
    # 129: {"act_category__category": '클래스', "loc__contains": '제주시'}, 128: {"act_category__category": '체험', "loc__contains": '제주시'},
    # 127: {"act_category__type": '익스트림액티비티', "loc__contains": '제주시'}, 126: {"act_category__type": '승마', "loc__contains": '제주시'}, 125: {"act_category__type": '수상액티비티', "loc__contains": '제주시'},
    # 124: {"act_category__type": '서핑', "loc__contains": '제주시'}, 123: {"act_category__type": '레이싱', "loc__contains": '제주시'},
    # 122: {"act_category__category": '액티비티', "loc__contains": '제주시'}, 121: {"loc__contains": '제주시'},

    def activity_find(self, intent):
        # 제주 : 121 - 132,
        # 132: '제주 액티비티 요가 추천', 131: '제주 액티비티 요리 추천', 130: '제주 액티비티 공예 추천',129: '제주 액티비티 클래스 추천', 128: '제주 액티비티 체험 추천',
        # 127: '제주 액티비티 익스트림액티비티 추천', 126: '제주 액티비티 승마 추천', 125: '제주 액티비티 수상액티비티 추천', 124: '제주 액티비티 서핑 추천',
        # 123: '제주 액티비티 레이싱 추천', 122: '제주 액티비티 중 추천', 121: '제주 전체 액티비티 추천',
        # 서귀포 : 133 - 144
        # 144: '서귀포 액티비티 요가 추천', 143: '서귀포 액티비티 요리 추천', 142: '서귀포 액티비티 공예 추천', 141: '서귀포 액티비티 클래스 추천', 140: '서귀포 액티비티 체험 추천',
        # 139: '서귀포 액티비티 익스트림액티비티 추천', 138: '서귀포 액티비티 승마 추천', 137: '서귀포 액티비티 수상액티비티 추천', 136: '서귀포 액티비티 서핑 추천',
        # 135: '서귀포 액티비티 레이싱 추천', 134: '서귀포 액티비티 중 추천', 133: '서귀포 전체 액티비티 추천'
        for i in intent[1]:
            if i == 'loc__contains':
                answer = Activity.objects.filter(loc__contains=intent[1]['loc__contains']).values().order_by('?').first()
                return answer
            elif i == 'act_category__category' and 'loc__contains':
                answer = Activity.objects.filter(loc__contains=intent[1]['loc__contains'],
                                                act_category__category=intent[1]['act_category__category']).values().order_by('?').first()
                return answer
            elif i == 'act_category__type' and 'loc__contains':
                answer = Activity.objects.filter(loc__contains=intent[1]['loc__contains'],
                                                act_category__type=intent[1]['act_category__type']).values().order_by('?').first()
                return answer
            else:
                answer = None
                return answer
        # if 121 <= intent[0] <= 132 :
        #     activity = Activity.objects.filter(loc__contains='제주시')
        #     # answer = Chatbot.objects.filter(label=label).values('answer').order_by('?').first()
        #     if intent[0] == 121:  # 제주 전체 액티비티 추천
        #         answer = activity.values().order_by('?').first()
        #     elif intent[0] == 122:  # 제주 액티비티 중 추천
        #         answer = activity.filter(act_category__category="액티비티").values().order_by('?').first()
        #     elif intent[0] == 123:  # 제주 액티비티 레이싱 추천
        #         answer = activity.filter(act_category__type="레이싱").values().order_by('?').first()
        #     elif intent[0] == 124:  # 제주 액티비티 서핑 추천
        #         answer = activity.filter(act_category__type="서핑").values().order_by('?').first()
        #     elif intent[0] == 125:  # 제주 액티비티 수상액티비티 추천
        #         answer = activity.filter(act_category__type="수상액티비티").values().order_by('?').first()
        #     elif intent[0] == 126:  # 제주 액티비티 승마 추천
        #         answer = activity.filter(act_category__type="승마").values().order_by('?').first()
        #     elif intent[0] == 127:  # 제주 액티비티 익스트림액티비티 추천
        #         answer = activity.filter(act_category__type="익스트림액티비티").values().order_by('?').first()
        #     elif intent[0] == 128:  # 제주 액티비티 체험 추천
        #         answer = activity.filter(act_category__category="체험").values().order_by('?').first()
        #     elif intent[0] == 129:  # 제주 액티비티 클래스 추천
        #         answer = activity.filter(act_category__category="클래스").values().order_by('?').first()
        #     elif intent[0] == 130:  # 제주 액티비티 공예 추천
        #         answer = activity.filter(act_category__type="공예").values().order_by('?').first()
        #     elif intent[0] == 131:  # 제주 액티비티 요리 추천
        #         answer = activity.filter(act_category__type="요리").values().order_by('?').first()
        #     elif intent[0] == 132:  # 제주 액티비티 요가 추천
        #         answer = activity.filter(act_category__type="요가").values().order_by('?').first()
        #
        # elif 133 <= intent[0] <= 144:
        #     activity = Activity.objects.filter(loc__contains='제주시')
        #     # answer = Chatbot.objects.filter(label=label).values('answer').order_by('?').first()
        #     if intent[0] == 133:  # 서귀포 전체 액티비티 추천
        #         answer = activity.values().order_by('?').first()
        #     elif intent[0] == 134:  # 서귀포 액티비티 중 추천
        #         answer = activity.filter(act_category__category="액티비티").values().order_by('?').first()
        #     elif intent[0] == 135:  # 서귀포 액티비티 레이싱 추천
        #         answer = activity.filter(act_category__type="레이싱").values().order_by('?').first()
        #     elif intent[0] == 136:  # 서귀포 액티비티 서핑 추천
        #         answer = activity.filter(act_category__type="서핑").values().order_by('?').first()
        #     elif intent[0] == 137:  # 서귀포 액티비티 수상액티비티 추천
        #         answer = activity.filter(act_category__type="수상액티비티").values().order_by('?').first()
        #     elif intent[0] == 138:  # 서귀포 액티비티 승마 추천
        #         answer = activity.filter(act_category__type="승마").values().order_by('?').first()
        #     elif intent[0] == 139:  # 서귀포 액티비티 익스트림액티비티 추천
        #         answer = activity.filter(act_category__type="익스트림액티비티").values().order_by('?').first()
        #     elif intent[0] == 140:  # 서귀포 액티비티 체험 추천
        #         answer = activity.filter(act_category__category="체험").values().order_by('?').first()
        #     elif intent[0] == 141:  # 서귀포 액티비티 클래스 추천
        #         answer = activity.filter(act_category__category="클래스").values().order_by('?').first()
        #     elif intent[0] == 142:  # 서귀포 액티비티 공예 추천
        #         answer = activity.filter(act_category__type="공예").values().order_by('?').first()
        #     elif intent[0] == 143:  # 서귀포 액티비티 요리 추천
        #         answer = activity.filter(act_category__type="요리").values().order_by('?').first()
        #     elif intent[0] == 144:  # 서귀포 액티비티 요가 추천
        #         answer = activity.filter(act_category__type="요가").values().order_by('?').first()
        #
        # else:
        #     answer = None
        #
        # return answer

    def activity_answer(self, intent):
        answer = self.activity_find(intent)

        if answer != None:
            answer_type = ActivityCategory.objects.get(id=answer['act_category_id']).type
            # print(answer_type)
            return f"{answer_type}를 할 수 있는 \n {answer['name']}을 추천합니다. \n {answer['name']}의 영업시간은 \n {answer['start_business_time']} - {answer['end_business_time']} \n 입니다." \
                   f"\n 예상 체험 시간은 {answer['time']} 입니다. \n 위치는\n {answer['loc']} 입니다."
        else:
            return f"{intent[1]['loc__contains']}에 추천할 체험 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다."
            # if 121 <= intent[0] <= 132:
            #     return '제주에 추천할 체험 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
            # elif 133 <= intent[0] <= 144:
            #     return '서귀포에 추천할 체험 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'


    # 160: {"res_category__type__contains" : '주점', "loc__contains": '서귀포'}, 159: {"res_category__type__contains" : '카페', "loc__contains": '서귀포'},
    # 158: {"res_category__type__in" : ["한식", "향토음식"], "loc__contains": '서귀포'}, 157: {"res_category__type" : '해물,생선요리', "loc__contains": '서귀포'},
    # 156: {"res_category__type" : '돼지고기구이', "loc__contains": '서귀포'}, 155: {"recommend__contains" : '국수', "loc__contains": '서귀포'},
    # 154: {"recommend__contains" : '갈치', "loc__contains": '서귀포'}, 153: {"loc__contains": '서귀포'},
    # 152: {"res_category__type__contains" : '주점', "loc__contains": '제주시'}, 151: {"res_category__type__contains" : '카페', "loc__contains": '제주시'},
    # 150: {"res_category__type__in" : ["한식", "향토음식"], "loc__contains": '제주시'}, 149: {"res_category__type" : '해물,생선요리', "loc__contains": '제주시'},
    # 148: {"res_category__type" : '돼지고기구이', "loc__contains": '제주시'}, 147: {"recommend__contains" : '국수', "loc__contains": '제주시'},
    # 146: {"recommend__contains" : '갈치', "loc__contains": '제주시'}, 145: {"loc__contains": '제주시'},
    def restaurant_find(self, intent):
        # 145 - 152 : 제주
            # 152: '제주 주점 맛집 추천', 151: '제주 카페 추천', 150: '제주 한식 맛집 추천', 149: '제주 생선요리 추천', 148: '제주 돼지고기구이 맛집 추천',
            # 147: '제주 국수 맛집 추천', 146: '제주 갈치 맛집 추천', 145: '제주 맛집 추천',
        # 153 - 160 : 서귀포
            # 160: '서귀포 주점 맛집 추천', 159: '서귀포시 카페 추천', 158: '서귀포 한식 맛집 추천', 157: '서귀포 생선요리 추천', 156: '서귀포 돼지고기구이 맛집 추천',
            # 155: '서귀포 국수 맛집 추천', 154: '서귀포 갈치 맛집 추천', 153: '서귀포 맛집 추천',
        for i in intent[1]:
            if i == 'loc__contains':
                answer = Restaurant.objects.filter(loc__contains=intent[1]['loc__contains']).values().order_by('?').first()
                return answer
            elif i == 'recommend__contains' and 'loc__contains':
                answer = Restaurant.objects.filter(loc__contains=intent[1]['loc__contains'],
                                                   recommend__contains=intent[1]['recommend__contains']).values().order_by('?').first()
                return answer
            elif i == 'res_category__type' and 'loc__contains':
                answer = Restaurant.objects.filter(loc__contains=intent[1]['loc__contains'],
                                                   res_category__type=intent[1]['res_category__type']).values().order_by('?').first()
                return answer
            elif i == 'res_category__type__in' and 'loc__contains':
                answer = Restaurant.objects.filter(loc__contains=intent[1]['loc__contains'],
                                                   res_category__type__in=intent[1]['res_category__type__in']).values().order_by('?').first()
                return answer
            elif i == 'res_category__type__contains' and 'loc__contains':
                answer = Restaurant.objects.filter(loc__contains=intent[1]['loc__contains'],
                                                   res_category__type__contains=intent[1]['res_category__type__contains']).values().order_by('?').first()
                return answer
            else:
                answer = None
                return answer
        # if 145 <= intent <= 152:
        #     restaurant = Restaurant.objects.filter(loc__contains='제주시')
        #     # answer = Chatbot.objects.filter(label=label).values('answer').order_by('?').first()
        #     if intent == 145:  # 제주 맛집 추천
        #         answer = restaurant.values().order_by('?').first()
        #     elif intent == 146:  # 제주 갈치 맛집 추천
        #         answer = restaurant.filter(recommend__contains="갈치").values().order_by('?').first()
        #     elif intent == 147:  # 제주 국수 맛집 추천
        #         answer = restaurant.filter(recommend__contains="국수").values().order_by('?').first()
        #     elif intent == 148:  # 제주 돼지고기구이 맛집 추천
        #         answer = restaurant.filter(res_category__type="돼지고기구이").values().order_by('?').first()
        #     elif intent == 149:  # 제주 생선요리 추천
        #         answer = restaurant.filter(res_category__type="해물,생선요리").values().order_by('?').first()
        #     elif intent == 150:  # 제주 한식 맛집 추천
        #         answer = restaurant.filter(res_category__type__in=["한식", "향토음식"]).values().order_by('?').first()
        #     elif intent == 151:  # 제주 카페 추천
        #         answer = restaurant.filter(res_category__type__contains="카페").values().order_by('?').first()
        #     elif intent == 152:  # 제주 주점 맛집 추천
        #         answer = restaurant.filter(res_category__type__contains="주점").values().order_by('?').first()
        # elif 153 <= intent <= 160:
        #     restaurant = Restaurant.objects.filter(loc__contains='서귀포')
        #     # answer = Chatbot.objects.filter(label=label).values('answer').order_by('?').first()
        #     if intent == 153:  # 서귀포 맛집 추천
        #         answer = restaurant.values().order_by('?').first()
        #     elif intent == 154:  # 서귀포 갈치 맛집 추천
        #         answer = restaurant.filter(recommend__contains="갈치").values().order_by('?').first()
        #     elif intent == 155:  # 서귀포 국수 맛집 추천
        #         answer = restaurant.filter(recommend__contains="국수").values().order_by('?').first()
        #     elif intent == 156:  # 서귀포 돼지고기구이 맛집 추천
        #         answer = restaurant.filter(res_category__type="돼지고기구이").values().order_by('?').first()
        #     elif intent == 157:  # 서귀포 생선요리 추천
        #         answer = restaurant.filter(res_category__type="해물,생선요리").values().order_by('?').first()
        #     elif intent == 158:  # 서귀포 한식 맛집 추천
        #         answer = restaurant.filter(res_category__type__in=["한식", "향토음식"]).values().order_by('?').first()
        #     elif intent == 159:  # 서귀포 카페 추천
        #         answer = restaurant.filter(res_category__type__contains="카페").values().order_by('?').first()
        #     elif intent == 160:  # 서귀포 주점 맛집 추천
        #         answer = restaurant.filter(res_category__type__contains="주점").values().order_by('?').first()
        # else:
        #     answer = None
        #
        # return answer

    def restaurant_answer(self, intent):

        answer = self.restaurant_find(intent)

        if answer != None:
            answer_type = RestaurantCategory.objects.get(id=answer['res_category_id']).type
            print(answer_type)
            return f" {answer_type} 맛집인 \n {answer['name']}을 추천합니다. \n {answer['name']}의 대표 메뉴는 \n {answer['recommend']} 입니다." \
                   f"\n 위치는\n {answer['loc']} 입니다."
        else:
            return f"{intent[1]['loc__contains']}에 추천할 식당 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다."
            # if 145 <= intent[0] <= 152:
            #     print(intent[0])
            #     return '제주에 추천할 식당 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
            # elif 153 <= intent[0] <= 160:
            #     return '서귀포에 추천할 식당 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'

    def shop_answer(self, intent):

        answer = Shop.objects.filter(loc__contains= intent[1]['loc__contains']).values().order_by('?').first()
        if answer != None:
            return f"{answer['name']}을 방문해 보시는 건 어떠세요? \n {answer['name']}는 \n  {answer['explanation']} \n {answer['loc']}에 위치하고 있습니다. "
        else:
            return f"{intent[1]['loc__contains']}에 추천할 쇼핑지 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다."
        # if intent[0] == 161:
        #     answer = Shop.objects.filter(loc__contains='제주시').values().order_by('?').first()
        #     if answer != None:
        #         return f"{answer['name']}을 방문해 보시는 건 어떠세요? \n {answer['name']}는 \n  {answer['explanation']} \n {answer['loc']}에 위치하고 있습니다. "
        #     else:
        #         return '제주에 추천할 쇼핑지 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        # elif intent[0] == 162:
        #     answer = Shop.objects.filter(loc__contains='서귀포').values().order_by('?').first()
        #     if answer != None:
        #         return f"{answer['name']}을 방문해 보시는 건 어떠세요? \n {answer['name']}는 \n  {answer['explanation']} \n {answer['loc']}에 위치하고 있습니다. "
        #     else:
        #         return '서귀포에 추천할 쇼핑지 정보가 없습니다. 이후, 업로드하여 더 나은 서비스로 찾아뵙겠습니다.'
        # else:
        #     return '알 수 없습니다.'


class Chat():

    def __init__(self):
        self.GMP_list = ['김포', '서울', '인천', '경기도', '김포공항', '인천공항']
        self.PUS_list = ['김해', '부산', '김해공항', '경남', '경상남도']
        self.TAE_list = ['대구', '경북', '대구공항', '울산']
        self.KWJ_list = ['광주', '광주공항']
        self.CJJ_list = ['청주', '청주공항']
        self.animal_list = ['강아지', '개', '멍멍이', '애견동물', '반려동물', '야옹이', '고슴도치', '너구리', '사막여우', '북극여우', '여우', '스컹크', '라쿤', '고양이',
                           '수달', '미어캣', '햄스터', '다람쥐', '하늘다람쥐', '쥐', '생쥐', '기니피그', '카피바라', '새', '구관조', '참새', '닭', '병아리', '오리',
                           '거위', '비둘기', '앵무새', '자라', '거북', '거북이', '도마뱀', '뱀', '개구리', '장수풍뎅이', '사슴벌레', '장수풍뎅이', '사슴벌레', '토끼']
        self.preferred_list = ['선생님', '은사님', '중요한 사람', '소중한 사람', '귀하신 분', '고마운 사람', '중요한 분', '중요한 분들', '고마우신 분']
        self.club_list = ['동호회', '친구 가족', '지인', '동창', '동창 가족 모임', '가족 모임']
        self.company_list = ['회사동료', '동료', '직장동료', '직장친구', '직장상사', ]
        self.relation_list = self.animal_list+self.preferred_list+self.club_list+self.company_list
        self.air_list = self.GMP_list+self.PUS_list+self.TAE_list+self.KWJ_list+self.CJJ_list


    def test_air(self, sentence):
        GMPs = self.GMP_list
        PUSs = self.PUS_list
        TAEs = self.TAE_list
        KWJs = self.KWJ_list
        CJJs = self.CJJ_list
        if any(i in sentence for i in PUSs) == True:
            return 'PUS'
        elif any(i in sentence for i in TAEs) == True:
            return 'TAE'
        elif any(i in sentence for i in KWJs) == True:
            return 'KWJ'
        elif any(i in sentence for i in CJJs) == True:
            return 'CJJ'
        else:
            return 'GMP'


    def test_with(self, sentence):
        animal = self.animal_list
        preferred = self.preferred_list
        club = self.club_list
        company = self.company_list
        if any(i in sentence for i in animal) == True:
            return '반려동물'
        elif any(i in sentence for i in preferred) == True:
            return '중요한 분'
        elif any(i in sentence for i in club) == True:
            return '친구분들'
        elif any(i in sentence for i in company) == True:
            return '회사분들'
        else:
            return '동행자'





if __name__ == '__main__':
    answer = []
    p = re.compile(r"제주시+")
    m = p.search('asdf ad 제주시 ㅁㄴㅁㄴㅁㄴㄴ')
    print(m.group())
    tourism = Tourism.objects.filter(address__contains='제주시')
    [answer.append(i['name']) for i in tourism.values('name')]
    print(f'1::::::::::::: {answer}')
    tourism = Tourism.objects.all()
    [answer.append(i['name']) for i in tourism.values('name')]
    print(f'2::::::::::::: {answer}')