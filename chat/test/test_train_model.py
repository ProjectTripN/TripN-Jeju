# 필요한 모듈 임포트
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate

from chat.test.test_preprocess import Preprocess


class TrainModel:

    def __init__(self):
        pass

    def createModel(self):
        # 데이터 읽어오기
        train_file = "chat/test/data/Q&A_L.csv"
        data = pd.read_csv(train_file, delimiter=',')
        queries = data['question'].tolist()
        intents = data['intent'].tolist()


        p = Preprocess(word2index_dic='chat/test/data/chatbot_dict.bin',
                       userdic='chat/test/data/user_dic.tsv')

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
        model.save('intent_model.h5')

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

        # intent : intents
        self.labels = {162: '서귀포 쇼핑몰 추천', 161: '제주 쇼핑몰 추천', 160: '서귀포 주점 맛집 추천', 159: '서귀포시 카페 추천', 158: '서귀포 한식 맛집 추천',
                     157: '서귀포 생선요리 추천', 156: '서귀포 돼지고기구이 맛집 추천', 155: '서귀포 국수 맛집 추천', 154: '서귀포 갈치 맛집 추천', 153: '서귀포 맛집 추천',
                     152: '제주 주점 맛집 추천', 151: '제주 카페 추천', 150: '제주 한식 맛집 추천', 149: '제주 생선요리 추천', 148: '제주 돼지고기구이 맛집 추천', 147: '제주 국수 맛집 추천',
                     146: '제주 갈치 맛집 추천', 145: '제주 맛집 추천', 144: '서귀포 액티비티 요가 추천', 143: '서귀포 액티비티 요리 추천', 142: '서귀포 액티비티 공예 추천', 141: '서귀포 액티비티 클래스 추천',
                     140: '서귀포 액티비티 체험 추천', 139: '서귀포 액티비티 익스트림액티비티 추천', 138: '서귀포 액티비티 승마 추천', 137: '서귀포 액티비티 수상액티비티 추천', 136: '서귀포 액티비티 서핑 추천',
                     135: '서귀포 액티비티 레이싱 추천', 134: '서귀포 액티비티 중 추천', 133: '서귀포 전체 액티비티 추천', 132: '제주 액티비티 요가 추천', 131: '제주 액티비티 요리 추천', 130: '제주 액티비티 공예 추천',
                     129: '제주 액티비티 클래스 추천', 128: '제주 액티비티 체험 추천', 127: '제주 액티비티 익스트림액티비티 추천', 126: '제주 액티비티 승마 추천', 125: '제주 액티비티 수상액티비티 추천',
                     124: '제주 액티비티 서핑 추천', 123: '제주 액티비티 레이싱 추천', 122: '제주 액티비티 중 추천', 121: '제주 전체 액티비티 추천', 120: '서귀포시 오름 추천', 119: '서귀포시 해수욕장 추천',
                     118: '서귀포 투어리즘 명소 추천', 117: '서귀포 투어리즘 추천', 116: '제주 오름 추천', 115: '제주 해수욕장 추천', 114: '제주 투어리즘 명소 추천', 113: '제주 투어리즘 추천',
                     112: '특정 요일 서귀포 날씨', 111: '서귀포 특정 월일 날씨', 110: '서귀포 특정일 날씨', 109: '2 일 뒤 서귀포시 날씨', 108: '서귀포 내일 날씨', 107: '서귀포 오늘 날씨', 106: '특정 요일 제주 날씨',
                     105: '제주 특정 월일 날씨', 104: '제주 특정일 날씨', 103: '2 일 뒤 제주 날씨', 102: '제주 내일 날씨', 101: '제주 오늘 날씨', 0: 'SNS 회원 로그인', 1: 'SNS 회원 연동 해체',
                     2: '결제 내역 확인', 3: '결제 영수증', 4: '결제 전 예약 변경', 5: '결제 카드 변경', 6: '결제 카드 할부 범위', 7: '결제 확인', 8: '대한항공 수화물', 9: '미성년자 회원 가입',
                     10: '비밀번호 변경', 11: '비밀번호 오류', 12: '비행 탑승 귀통증', 13: '숙박 객실 변경', 14: '숙박 객실 유형', 15: '숙박 객실 추가', 16: '숙박 결제 취소', 17: '숙박 당일 예약',
                     18: '숙박 당일 취소', 19: '숙박 딜레이 체크인', 20: '숙박 미성년자 이용 가능', 21: '숙박 사전 객실 배정', 22: '숙박 애완동물 동반', 23: '숙박 예약 대기', 24: '숙박 이용 가능인원 확인',
                     25: '숙박 이용객 확인', 26: '숙박 체크인 바우처 필요', 27: '숙박 체크인 절차', 28: '숙박 추가 요금', 29: '숙박 퇴실 시간 확인', 30: '숙박 퇴실 연장', 31: '숙박 퇴실 확인',
                     32: '숙박 현장 추가 결제 확인', 33: '아시아나항공 수화물', 34: '애완 동반 비행', 35: '에어부산 수화물', 36: '에어서울 수화물', 37: '예약 내역 변경', 38: '예약 내역 확인', 39: '예약 외국인 가능',
                     40: '예약 최소 출발일', 41: '예약 취소', 42: '예약 환불 규정', 43: '예약완료시 예약 확정 확인', 44: '임산부 비행 확인', 45: '전화 상의 카드 결제', 46: '제주항공 수화물', 47: '좌석확인',
                     48: '좌석확정확인', 49: '진에어 수화물', 50: '출국 - 입국확인', 51: '카드 결제 취소 확인', 52: '타인 카드 결제', 53: '티웨이항공 수화물', 54: '항공 e - ticket',
                     55: '항공 결제 수단 변경', 56: '항공 결제 완료 확인', 57: '항공 기상 취소', 58: '항공 노쇼', 59: '항공 수수료', 60: '항공 수화물', 61: '항공 스케줄 변경', 62: '항공 스케줄 확인 필요',
                     63: '항공 예약 변경', 64: '항공 예약 사전 좌석 배정', 65: '항공 예약 취소', 66: '항공 외국인 탑승자', 67: '항공 요금', 68: '항공 요금 변경', 69: '항공 탑승 신분증',
                     70: '항공권 결제', 71: '항공권 예약 변경', 72: '항공권 예약 수정', 73: '항공권 예약 양도', 74: '항공권 예약 완료 후 취소', 75: '항공사 취소 수수료',76: '항공정보수정',
                     77: '회원 아이디 변경', 78: '회원 정보 수정', 79: '회원 탈퇴', 80: '회원가입 본인인증 실명확인', 81: '회원가입 본인인증 오류', 82: '회원가입 휴대폰 본인인증 오류', 83: '회원정보 변경'}

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
        self.p = Preprocess(word2index_dic='chat/test/data/chatbot_dict.bin', userdic='chat/test/data/user_dic.tsv')
        self.intent = IntentModel(model_name='chat/test/intent_model.h5', proprocess=self.p)

    def predict_test(self, question):
        predict = self.intent.predict_class(question)
        predict_label = self.intent.labels[predict]

        print(f'의도 예측 클래스 : {predict}')
        print(f'의도 예측 레이블 : {predict_label}')

        return predict


if __name__ == '__main__':
    # TrainModel = TrainModel()
    # TrainModel.createModel()

    p = Preprocess(word2index_dic='./data/chatbot_dict.bin', userdic='./data/user_dic.tsv')

    intent = IntentModel(model_name='./intent_model.h5', proprocess=p)

    question = '예쁜 카페 알려줘'

    predict = intent.predict_class(question)
    predict_label = intent.labels[predict]

    print(question)
    print(f'의도 예측 클래스 : {predict}')
    print(f'의도 예측 레이블 : {predict_label}')