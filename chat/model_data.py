import csv

from chat.models import Chatbot
from common.models import ValueObject, Reader, Printer


class ChatDbUploader:

    def __init__(self):
        vo = ValueObject()
        reader = Reader()
        self.printer = Printer()
        vo.context = 'chat/test/data/'
        vo.fname = 'train.csv'
        self.csvfile = reader.new_file(vo)

    def insert_data(self):
        print('############ 2 ##########')
        self.insert_chatDB()
        print('############ 3 ##########')


    def insert_chatDB(self):
        with open(self.csvfile, newline='', encoding='utf8') as f:
            data_reader = csv.DictReader(f)
            for row in data_reader:
                if not Chatbot.objects.filter(answer=row['answer']).exists():
                    chat = Chatbot.objects.create(answer=row['answer'],
                                                  category=row['category'],
                                                  detailedCategory=row['detailedCategory'],
                                                  intents=row['intents'],
                                                  intentNumber=row['intent'],
                                                  label=row['label'],)
                    print(f'chat : {chat}')

        print('Chat DATA UPLOADED SUCCESSFULY!')
