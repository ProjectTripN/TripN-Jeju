import datetime as dt
from datetime import datetime

import requests

# Create your tests here.


class Weather(object):
    def __init__(self):
        pass

    def process(self):
        return self.weather_now()

    def weather_now(self):
        base_date, base_time, nx, ny = self.weather_api()
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        params = {
            'serviceKey': 'Azs8t5lc5MVlv67BnCCXpwjGc9eLdowYV2q3MZO0wqwOkWo3vpUP0PsHimKL0osXusxlIb+888C2E+PquYdixQ==',
            'pageNo': '1',
            'numOfRows': '10',
            'dataType': 'JSON',
            'base_date': base_date,
            'base_time': base_time,
            'nx': f'{nx}',
            'ny': f'{ny}'}
        response = requests.get(url, params=params)
        weather = response.json().get('response').get('body').get('items')
        weather = list(weather.values())[0]
        for i in weather:
            if i['category'] == 'SKY':
                sky = i
            elif i['category'] == 'PTY':
                pty = i
        # print(f'SKY dict : {sky}')
        # print(f'PTY dict : {pty}')
        # print(f'SKY result : {sky["fcstValue"]}')
        # print(f'PTY result : {pty["fcstValue"]}')
        return self.weather_transfer(sky, pty)

    def weather_pre(self, nx, ny):
        base_date, base_time= self.weather_api()
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        params = {
            'serviceKey': 'Azs8t5lc5MVlv67BnCCXpwjGc9eLdowYV2q3MZO0wqwOkWo3vpUP0PsHimKL0osXusxlIb+888C2E+PquYdixQ==',
            'pageNo': '1',
            'numOfRows': '1000',
            'dataType': 'JSON',
            'base_date': base_date,
            'base_time': base_time,
            'nx': f'{nx}',
            'ny': f'{ny}'}
        # print(params)
        response = requests.get(url, params=params)
        # print(response.url)
        weather = response.json().get('response').get('body').get('items')
        weather = list(weather.values())[0]
        time = str((int(base_time) + 100)) if int(base_time) + 100 < 2400 else "0000"
        time = time if len(time) == 4 else f'0{time}'
        day = [base_date, self.date_string(datetime.now() + dt.timedelta(days=1)), self.date_string(datetime.now() + dt.timedelta(days=2))]
        sky, pty, tmp = [], [], []
        for i in weather:
            if i['fcstDate'] == base_date and i['fcstTime'] == time:
                if i['category'] == 'SKY':
                    sky.append(i)
                elif i['category'] == 'PTY':
                    pty.append(i)
                elif i['category'] == 'TMP':
                    tmp.append(i)
            elif i['fcstDate'] == day[1] and i['fcstTime'] == time:
                if i['category'] == 'SKY':
                    sky.append(i)
                elif i['category'] == 'PTY':
                    pty.append(i)
                elif i['category'] == 'TMP':
                    tmp.append(i)
            elif i['fcstDate'] == day[2] and i['fcstTime'] == time:
                if i['category'] == 'SKY':
                    sky.append(i)
                elif i['category'] == 'PTY':
                    pty.append(i)
                elif i['category'] == 'TMP':
                    tmp.append(i)
        result = [self.weather_transfer(sky[i], pty[i]) for i in range(len(sky))]
        tmp = [i['fcstValue'] for i in tmp]
        return {j : [result[i], tmp[i]] for i, j in enumerate(day)}

    def weather_api(self):
        # 현재 시간
        now = datetime.now()
        base_date = self.date_string(now)
        # 1일 총 8번 데이터가 업데이트 된다.(0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300)
        # 현재 api를 가져오려는 시점의 이전 시각에 업데이트된 데이터를 base_time, base_date로 설정
        if now.hour < 2 or (now.hour == 2 and now.minute <= 10):  # 0시~2시 10분 사이
            base_time = "2300"
        elif now.hour < 5 or (now.hour == 5 and now.minute <= 10):  # 2시 11분~5시 10분 사이
            base_time = "0200"
        elif now.hour < 8 or (now.hour == 8 and now.minute <= 10):  # 5시 11분~8시 10분 사이
            base_time = "0500"
        elif now.hour <= 11 or now.minute <= 10:  # 8시 11분~11시 10분 사이
            base_time = "0800"
        elif now.hour < 14 or (now.hour == 14 and now.minute <= 10):  # 11시 11분~14시 10분 사이
            base_time = "1100"
        elif now.hour < 17 or (now.hour == 17 and now.minute <= 10):  # 14시 11분~17시 10분 사이
            base_time = "1400"
        elif now.hour < 20 or (now.hour == 20 and now.minute <= 10):  # 17시 11분~20시 10분 사이
            base_time = "1700"
        elif now.hour < 23 or (now.hour == 23 and now.minute <= 10):  # 20시 11분~23시 10분 사이
            base_time = "2000"
        else:  # 23시 11분~23시 59분
            base_time = "2300"
        return base_date, base_time

    def date_string(self, date):
        return f'{date.year}{date.month if date.month > 9 else f"0{date.month}"}{date.day if date.day > 9 else f"0{date.day}"}'

    def weather_transfer(self, sky, pty):
        return self.sky_transfer(sky["fcstValue"]) if self.pty_transfer(pty["fcstValue"]) == '0' else self.pty_transfer(
            pty["fcstValue"])

    # 하늘상태(SKY) 코드 : 맑음(1), 구름많음(3), 흐림(4)
    def sky_transfer(self, sky):
        if sky == '1':
            return '맑음'
        elif sky == '3':
            return '구름 많음'
        elif sky == '4':
            return '흐림'
        else:
            return '데이터 없음'

    # 강수형태(PTY) 코드 : (단기) 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)
    def pty_transfer(self, pty):
        if pty == '0':
            return '0'
        elif pty == '1':
            return '비'
        elif pty == '2':
            return '비, 눈'
        elif pty == '3':
            return '눈'
        elif pty == '4':
            return '소나기'
        else:
            return '데이터 없음'


if __name__ == '__main__':
    w = Weather()
    today = dt.datetime.now()
    tom = dt.datetime.now() + dt.timedelta(days=1)
    ttom = dt.datetime.now() + dt.timedelta(days=2)
    today = str(today)[0:4] + str(today)[5:7] + str(today)[8:10]
    tom = str(tom)[0:4] + str(tom)[5:7] + str(tom)[8:10]
    ttom = str(ttom)[0:4] + str(ttom)[5:7] + str(ttom)[8:10]
    print(str(today)[0:4]+str(today)[5:7]+str(today)[8:10])

    print(w.weather_now())
    print(w.weather_pre()[today])
    print(w.weather_pre()[tom])
    print(w.weather_pre()[ttom])
    # print('*'*100)
