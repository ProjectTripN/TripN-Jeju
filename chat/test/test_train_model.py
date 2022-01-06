# 필요한 모듈 임포트
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate

from chat.test.test_preprocess import Preprocess
import datetime as dt

class TrainModel:

    def __init__(self):
        pass

    def createModel(self):
        # 데이터 읽어오기
        train_file = "data/train.csv"
        data = pd.read_csv(train_file, delimiter=',')
        queries = data['question'].tolist()
        intents = data['intent'].tolist()


        p = Preprocess(word2index_dic='data/chatbot_dict.bin',
                       userdic='data/user_dic_2.tsv')

        # 단어 시퀀스 생성
        sequences = []
        for sentence in queries:
            pos = p.pos(sentence)
            keywords = p.get_keywords(pos, without_tag=True)
            seq = p.get_wordidx_sequence(keywords)
            sequences.append(seq)

        # 단어 인덱스 시퀀스 벡터 ○2
        # 단어 시퀀스 벡터 크기
        MAX_SEQ_LEN = 25
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        # (105658, 15)
        print(padded_seqs.shape)
        print(len(intents))  # 105658

        # 학습용, 검증용, 테스트용 데이터셋 생성 ○3
        # 학습셋:검증셋:테스트셋 = 7:2:1
        ds = tf.data.Dataset.from_tensor_slices((padded_seqs, intents))
        ds = ds.shuffle(len(queries))

        train_size = int(len(padded_seqs) * 0.7)
        val_size = int(len(padded_seqs) * 0.2)
        test_size = int(len(padded_seqs) * 0.1)

        train_ds = ds.take(train_size).batch(20)
        val_ds = ds.skip(train_size).take(val_size).batch(20)
        test_ds = ds.skip(train_size + val_size).take(test_size).batch(20)

        # 하이퍼 파라미터 설정
        dropout_prob = 0.5
        EMB_SIZE = 128
        EPOCH = 50
        VOCAB_SIZE = len(p.word_index) + 1  # 전체 단어 개수

        # CNN 모델 정의  ○4
        input_layer = Input(shape=(MAX_SEQ_LEN,))
        embedding_layer = Embedding(VOCAB_SIZE, EMB_SIZE, input_length=MAX_SEQ_LEN)(input_layer)
        dropout_emb = Dropout(rate=dropout_prob)(embedding_layer)

        conv1 = Conv1D(filters=128, kernel_size=3, padding='valid', activation=tf.nn.relu)(dropout_emb)
        pool1 = GlobalMaxPool1D()(conv1)

        conv2 = Conv1D(filters=128, kernel_size=4, padding='valid', activation=tf.nn.relu)(dropout_emb)
        pool2 = GlobalMaxPool1D()(conv2)

        conv3 = Conv1D(filters=128, kernel_size=5, padding='valid', activation=tf.nn.relu)(dropout_emb)
        pool3 = GlobalMaxPool1D()(conv3)

        # 3,4,5gram 이후 합치기
        concat = concatenate([pool1, pool2, pool3])

        hidden = Dense(128, activation=tf.nn.relu)(concat)
        dropout_hidden = Dropout(rate=dropout_prob)(hidden)
        logits = Dense(163, name='logits')(dropout_hidden)
        predictions = Dense(163, activation=tf.nn.softmax)(logits)

        # 모델 생성  ○5
        model = Model(inputs=input_layer, outputs=predictions)
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # 모델 학습 ○6
        model.fit(train_ds, validation_data=val_ds, epochs=EPOCH, verbose=1)

        # 모델 평가(테스트 데이터 셋 이용) ○7
        loss, accuracy = model.evaluate(test_ds, verbose=1)
        print('Accuracy: %f' % (accuracy * 100))
        print('loss: %f' % (loss))

        # 모델 저장  ○8
        model.save('chat_model_3.h5')

        # def predictModel(self):
        #
        #     p = Preprocess(word2index_dic='./data/chatbot_dict.bin', userdic='./data/user_dic.tsv')
        #
        #     intent = IntentModel(model_name='./model/intent_model.h5', proprocess=p)
        #
        #     question = '내일 일정은 어때'
        #
        #     predict = intent.predict_class(question)
        #     predict_label = intent.labels[predict]

class IntentModel:
    def __init__(self, model_name, proprocess):
        self.MAX_SEQ_LEN = 25
        today = dt.datetime.now()
        tom = dt.datetime.now() + dt.timedelta(days=1)
        ttom = dt.datetime.now() + dt.timedelta(days=2)
        today = str(today)[0:4] + str(today)[5:7] + str(today)[8:10]
        tom = str(tom)[0:4] + str(tom)[5:7] + str(tom)[8:10]
        ttom = str(ttom)[0:4] + str(ttom)[5:7] + str(ttom)[8:10]

        # intent : intents
        self.labels = {162: {"loc__contains": '서귀포'}, 161: {"loc__contains": '제주'},
                       160: {"res_category__type__contains" : '주점', "loc__contains": '서귀포'}, 159: {"res_category__type__contains" : '카페', "loc__contains": '서귀포'},
                       158: {"res_category__type__in" : ["한식", "향토음식"], "loc__contains": '서귀포'}, 157: {"res_category__type" : '해물,생선요리', "loc__contains": '서귀포'},
                       156: {"res_category__type" : '돼지고기구이', "loc__contains": '서귀포'}, 155: {"recommend__contains" : '국수', "loc__contains": '서귀포'},
                       154: {"recommend__contains" : '갈치', "loc__contains": '서귀포'}, 153: {"loc__contains": '서귀포'},
                       152: {"res_category__type__contains" : '주점', "loc__contains": '제주시'}, 151: {"res_category__type__contains" : '카페', "loc__contains": '제주시'},
                       150: {"res_category__type__in" : ["한식", "향토음식"], "loc__contains": '제주시'}, 149: {"res_category__type" : '해물,생선요리', "loc__contains": '제주시'},
                       148: {"res_category__type" : '돼지고기구이', "loc__contains": '제주시'}, 147: {"recommend__contains" : '국수', "loc__contains": '제주시'},
                       146: {"recommend__contains" : '갈치', "loc__contains": '제주시'}, 145: {"loc__contains": '제주시'},

                       144: {"act_category__type": '요가', "loc__contains": '서귀포'}, 143: {"act_category__type": '요리', "loc__contains": '서귀포'},
                       142: {"act_category__type": '공예', "loc__contains": '서귀포'}, 141: {"act_category__category": '클래스', "loc__contains": '서귀포'},
                       140: {"act_category__category": '체험', "loc__contains": '서귀포'}, 139: {"act_category__type": '익스트림액티비티', "loc__contains": '서귀포'},
                       138: {"act_category__type": '승마', "loc__contains": '서귀포'}, 137: {"act_category__type": '수상액티비티', "loc__contains": '서귀포'}, 136: {"act_category__type": '서핑', "loc__contains": '서귀포'},
                       135: {"act_category__type": '레이싱', "loc__contains": '서귀포'}, 134: {"act_category__category": '액티비티', "loc__contains": '서귀포'}, 133: {"loc__contains": '서귀포'},
                       132: {"act_category__type": '요가', "loc__contains": '제주시'}, 131: {"act_category__type": '요리', "loc__contains": '제주시'}, 130: {"act_category__type": '공예', "loc__contains": '제주시'},
                       129: {"act_category__category": '클래스', "loc__contains": '제주시'}, 128: {"act_category__category": '체험', "loc__contains": '제주시'},
                       127: {"act_category__type": '익스트림액티비티', "loc__contains": '제주시'}, 126: {"act_category__type": '승마', "loc__contains": '제주시'}, 125: {"act_category__type": '수상액티비티', "loc__contains": '제주시'},
                       124: {"act_category__type": '서핑', "loc__contains": '제주시'}, 123: {"act_category__type": '레이싱', "loc__contains": '제주시'},
                       122: {"act_category__category": '액티비티', "loc__contains": '제주시'}, 121: {"loc__contains": '제주시'},


                       120: {"tour_category_id": 12, "address__contains": '서귀포'}, 119: {"tour_category_id__in": [1], "address__contains": '서귀포'},
                       118: {"tour_category_id__in": [1, 12], "address__contains": '서귀포'}, 117: {"address__contains": '서귀포'},
                       116: {"tour_category_id": 12, "address__contains": '제주시'}, 115: {"tour_category_id__in": [1], "address__contains": '제주시'},
                       114: {"tour_category_id__in": [1, 12], "address__contains": '제주시'}, 113: {"address__contains": '제주시'},

                       112: ['서귀포', 53, 33, '모레', ttom], 111: ['서귀포', 53, 33, '내일', tom], 110: ['서귀포', 53, 33, '오늘', today], 109: ['제주', 53, 38, '모레', ttom],
                       108: ['제주', 53, 38, '내일', tom], 107: ['제주', 53, 38, '오늘', today],
                       106: '12월 제주 날씨', 105: '11월 제주 날씨', 104: '10월 제주 날씨', 103: '09월 제주 날씨', 102: '08월 제주 날씨', 101: '07월 제주 날씨', 100: '06월 제주 날씨',
                       99: '05월 제주 날씨', 98: '04월 제주 날씨', 97: '03월 제주 날씨', 96: '02월 제주 날씨', 95: '01월 제주 날씨', 94: '겨울 제주 날씨', 93: '가을 제주 날씨', 92: '여름 제주 날씨',
                       91: '봄 제주 날씨', 0: '첫 인사', 1: '끝 인사', 2: '욕', 3: '결제 영수증', 4: '결제 전 예약 변경', 5: '결제 카드 변경', 6: '결제 카드 할부 범위', 7: '결제 확인',
                       8: '대한항공 수화물', 9: '미성년자 회원 가입', 10: '비밀번호 변경', 11: '비밀번호 오류', 12: '비행 탑승 귀통증', 13: '숙박 객실 변경', 14: '숙박 객실 유형', 15: '숙박 객실 추가',
                       16: '숙박 결제 취소', 17: '숙박 당일 예약', 18: '숙박 당일 취소', 19: '숙박 딜레이 체크인', 20: '숙박 미성년자 이용 가능', 21: '숙박 사전 객실 배정', 22: '숙박 애완동물 동반',
                       23: '숙박 예약 대기', 24: '숙박 이용 가능인원 확인', 25: '숙박 이용객 확인', 26: '숙박 체크인 바우처 필요', 27: '숙박 체크인 절차', 28: '숙박 추가 요금', 29: '숙박 퇴실 시간 확인',
                       30: '숙박 퇴실 연장', 31: '숙박 퇴실 확인', 32: '숙박 현장 추가 결제 확인', 33: '아시아나항공 수화물', 34: '애완 동반 비행', 35: '에어부산 수화물', 36: '에어서울 수화물',
                       37: '예약 내역 변경', 38: '예약 내역 확인', 39: '예약 외국인 가능', 40: '예약 최소 출발일', 41: '예약 취소', 42: '예약 환불 규정', 43: '예약완료시 예약 확정 확인', 44: '임산부 비행 확인',
                       45: '전화 상의 카드 결제', 46: '제주항공 수화물', 47: '좌석확인', 48: '좌석확정확인', 49: '진에어 수화물', 50: '출국 - 입국확인', 51: '카드 결제 취소 확인', 52: '타인 카드 결제',
                       53: '티웨이항공 수화물',  54: '항공 e - ticket', 55: '항공 결제 수단 변경', 56: '항공 결제 완료 확인', 57: '항공 기상 취소', 58: '항공 노쇼', 59: '항공 수수료', 60: '항공 수화물',
                       61: '항공 스케줄 변경', 62: '항공 스케줄 확인 필요', 63: '항공 예약 변경', 64: '항공 예약 사전 좌석 배정', 65: '항공 예약 취소', 66: '항공 외국인 탑승자', 67: '항공 요금',
                       68: '항공 요금 변경', 69: '항공 탑승 신분증', 70: '항공권 결제', 71: '항공권 예약 변경', 72: '항공권 예약 수정', 73: '항공권 예약 양도', 74: '항공권 예약 완료 후 취소',
                       75: '항공사 취소 수수료',76: '항공정보수정', 77: '회원 아이디 변경', 78: '회원 정보 수정', 79: '회원 탈퇴', 80: '회원가입 본인인증 실명확인', 81: '회원가입 본인인증 오류',
                       82: '회원가입 휴대폰 본인인증 오류', 83: '회원정보 변경', 84: 'SNS 회원 로그인', 85: 'SNS 회원 연동 해체', 86: '결제 내역 확인'}

        self.model= load_model(model_name)

        self.p = proprocess

    def predict_class(self, question):
        # 형태소 분석
        pos = self.p.pos(question)

        # 문장 내 키워드 추출(불용어 제거)\
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=self.MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]


class TestChat:
    def __init__(self):
        self.p = Preprocess(word2index_dic='chat/test/data/chatbot_dict.bin', userdic='chat/test/data/user_dic_2.tsv')
        self.intent = IntentModel(model_name='chat/test/chat_model.h5', proprocess=self.p)

    def predict_test(self, question):
        predict = self.intent.predict_class(question)
        predict_label = self.intent.labels[predict]

        print(f'의도 예측 클래스 : {predict}')
        print(f'의도 예측 레이블 : {predict_label}')

        return predict, predict_label


if __name__ == '__main__':
    TrainModel = TrainModel()
    TrainModel.createModel()

    question = "제주 갈치 맛집 알려줘"

    TestChat = TestChat()
    TestChat = TestChat.predict_test(question)
    print(TestChat[0])
    print(TestChat[1])
    for i in TestChat[1]:
        if i == 'loc__contains':
            print(TestChat[1]['loc__contains'])
            break
        if i == 'recommend__contains' and 'loc__contains':
            print(TestChat[1]['recommend__contains'])
            break
        else:
            print("dhohdohdohdohdohdodhodhdo")
            print(TestChat[1]['loc__contains'])
    # p = Preprocess(word2index_dic='./data/chatbot_dict.bin', userdic='./data/user_dic.tsv')
    #
    # intent = IntentModel(model_name='./intent_model.h5', proprocess=p)
    #
    # question = '예쁜 카페 알려줘'
    #
    # predict = intent.predict_class(question)
    # predict_label = intent.labels[predict]
    #
    # print(question)
    # print(f'의도 예측 클래스 : {predict}')
    # print(f'의도 예측 레이블 : {predict_label}')