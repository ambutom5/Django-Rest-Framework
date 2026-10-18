from django.db import models

# Create your models here.

class QuestionsDb(models.Model):
    question = models.CharField(max_length = 500)
    option_a = models.CharField(max_length = 100)
    option_b = models.CharField(max_length = 100)
    option_c = models.CharField(max_length = 100)
    option_d = models.CharField(max_length = 100)
    correct_answer = models.CharField(max_length = 100)
