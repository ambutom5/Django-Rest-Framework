from rest_framework import serializers
from ExamApp.models import QuestionsDb

class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length = 500)
    option_a = serializers.CharField(max_length =100)
    option_b = serializers.CharField(max_length =100)
    option_c = serializers.CharField(max_length =100)
    option_d = serializers.CharField(max_length =100)
    correct_answer = serializers.CharField(max_length = 100)