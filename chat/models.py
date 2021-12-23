from django.db import models

# Create your models here.

class Chatbot(models.Model):

    label = models.TextField()  # label
    category = models.TextField()
    detailedCategory = models.TextField()
    intents = models.TextField()
    intentNumber = models.IntegerField()
    answer = models.TextField()

    class Meta:
        db_table = "chatbot"

    def __str__(self):
        return f"id: {self.id}, intents: {self.intents}," \
               f" intentNumber: {self.intentNumber}, answer: {self.answer}"
