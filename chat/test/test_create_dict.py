#
# 챗봇에서 사용하는 사전 파일 생성
#

from tensorflow.keras import preprocessing
import pickle

# 말뭉치 데이터 읽어오기
from chat.test.test_preprocess import Preprocess

class CreateDict:

    def __init__(self):
        pass

    def read_corpus_data(self, filename):
        with open(filename, 'r', encoding='UTF-8') as f:
            data = [line.split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)", -1) for line in f.read().splitlines()]
            # data = data[1:]
        return data

    def create_dict(self):
        # 말뭉치 데이터 가져오기
        corpus_data = self.read_corpus_data('./data/Q&A_Q.csv')


        # 망뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
        p = Preprocess()
        dict = []
        for c in corpus_data:
            print(c)
            pos = p.pos(c[0])
            for k in pos:
                dict.append(k[0])
            # keywords = p.get_keywords(pos, without_tag=True)
            # for k in keywords:
            #     dict.append(k)

        # 사전에 사용될 word2index 생성
        # 사전의 첫번 째 인덱스에는 OOV 사용
        tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
        tokenizer.fit_on_texts(dict)
        word_index = tokenizer.word_index

        # 사전 파일 생성
        f = open("./data/chatbot_dict.bin", "wb")
        try:
            pickle.dump(word_index, f)
        except Exception as e:
            print(e)
        finally:
            f.close()

    def dict_test(self):
        # 단어 사전 불러오기
        f = open("./data/chatbot_dict.bin", "rb")
        word_index = pickle.load(f)
        f.close()

        sent = "병신 강아지같은사람아"

        # 전처리 객체 생성
        p = Preprocess(userdic='./data/user_dic_2.tsv')

        # 형태소분석기 실행
        pos = p.pos(sent)

        # 품사 태그 없이 키워드 출력
        keywords = p.get_keywords(pos, without_tag=True)
        for word in keywords:
            try:
                print(word, word_index[word])
            except KeyError:
                # 해당 단어가 사전에 없는 경우, OOV 처리
                print(word, word_index['OOV'])

if __name__ == '__main__':
    c = CreateDict()
    # c.create_dict()
    c.dict_test()