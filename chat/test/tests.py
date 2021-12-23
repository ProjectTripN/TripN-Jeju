from django.db import models
# Create your models here.
from konlpy.tag import Kkma

class Chatbot(object):
    def __init__(self):
        pass
    def kkma_execute(self):

        # 꼬꼬마 형태소 분석기 객체 생성
        kkma = Kkma()
        text = "아버지가 방에 들어갑니다."
        # 형태소 추출
        morphs = kkma.morphs(text)
        print(morphs)
        # 형태소와 품사 태그 추출
        pos = kkma.pos(text)
        print(pos)
        # 명사만 추출
        nouns = kkma.nouns(text)
        print(nouns)
        # 문장 분리
        sentences = "오늘 날씨는 어때요? 내일은 덥다던데."
        s = kkma.sentences(sentences)
        print(s)
if __name__=='__main__':
    c = Chatbot()
    c.kkma_execute()