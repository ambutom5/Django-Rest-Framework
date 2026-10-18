from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ExamApp.models import QuestionsDb
from ExamApp.serializers import QuestionSerializer

# Create your views here.

class QuestionListCreateView(APIView):
    def get(self,request):
        qs = QuestionsDb.objects.all()
        serializer_instance = QuestionSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = QuestionSerializer(data=form_data)
        if serializer_instance.is_valid():
            original_data = serializer_instance.validated_data
            QuestionsDb.objects.create(**original_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class QuestionRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = QuestionsDb.objects.get(id=pk)
        serializer_instance=QuestionSerializer(qs)
        return Response(data=serializer_instance.data)

    def delete(self,request,pk):
        QuestionsDb.objects.filter(id=pk).delete()
        return Response({"message":"Deleted!"})

    def put(self,request,pk):
        form_data = request.data
        serializer_instance = QuestionSerializer(data = form_data)
        if serializer_instance.is_valid():
            original_data = serializer_instance.validated_data
            QuestionsDb.objects.filter(id=pk).update(**original_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

    
