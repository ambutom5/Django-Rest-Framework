from rest_framework import serializers
from Repository.models import QuestionsDb,SubmissionDb

class QuestionsDbSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 100)
    language = serializers.ChoiceField(choices = QuestionsDb.LANGUAGE_CHOICES)
    difficulty_level = serializers.ChoiceField(choices = QuestionsDb.DIFFICULTY_CHOICES)
    topic = serializers.CharField(max_length = 100)
    score = serializers.IntegerField()
    published_date = serializers.DateTimeField(read_only = True)
    notes = serializers.CharField(max_length = 100)
    sample_input = serializers.CharField(max_length = 500)
    sample_output = serializers.CharField(max_length = 500)
    is_active = serializers.BooleanField(default = True)

class SubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()
    owner = serializers.CharField()
    points = serializers.IntegerField(read_only=True)
    submission_date = serializers.DateTimeField(read_only=True)
    remarks = serializers.CharField(read_only=True)

    def validate(self,validated_data):
        question_id = validated_data.get("question_id")
        if not QuestionsDb.objects.filter(id=question_id).exists():
            raise serializers.ValidationError("Question Doesnot Exists!")
        return validated_data