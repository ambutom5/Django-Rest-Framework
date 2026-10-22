from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Repository.models import QuestionsDb
from Repository.serializers import QuestionsDbSerializer
from Repository.models import SubmissionDb
from Repository.serializers import SubmissionSerializer

# Create your views here.

class QuestionsListCreateView(APIView):

    # def get(self,request):
    #     qs = QuestionsDb.objects.all().values()
    #     # print(qs)
    #     result = list(qs)
    #     return Response(data = result)

    # def post(self,request):
    #     form_data = request.data
    #     QuestionsDb.objects.create(**form_data)
    #     return Response(data={
    #         "message" : "Question Added Successfully!"
    #     })


    def get(self,request):
        qs = QuestionsDb.objects.all()
        serializer_instance = QuestionsDbSerializer(qs, many = True)     # Serialize the QuesrySet
        return Response(data = serializer_instance.data)                 # Returns the serialized data as a response
    
    
    def post(self,request):
        form_data = request.data
        serializer_instance = QuestionsDbSerializer(data=form_data)
        if serializer_instance.is_valid():
            original_data = serializer_instance.validated_data
            QuestionsDb.objects.create(**original_data)
            return Response(data={
             "message" : "Question Added Successfully!"
            })
        else:
            return Response(data = serializer_instance.errors)


class QuestionsRetrieveUpdataDeleteView(APIView):
    def get(self,request,pk):
        qs = QuestionsDb.objects.get(id=pk)
        serializer_instance = QuestionsDbSerializer(qs)
        return Response(data=serializer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        serializer_instance = QuestionsDbSerializer(data = form_data)
        if serializer_instance.is_valid():
            actual_data = serializer_instance.validated_data
            QuestionsDb.objects.filter(id=pk).update(**actual_data)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        QuestionsDb.objects.filter(id=pk).delete()
        return Response(data = {"message":"Question Deleted!"})


class SubmissionsListCreateView(APIView):
    def get(self,request):
        qs = SubmissionDb.objects.all()
        serializer_instance = SubmissionSerializer(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance=SubmissionSerializer(data=form_data)
        if serializer_instance.is_valid():
            org_data = serializer_instance.validated_data
            SubmissionDb.objects.create(**org_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class SubmissionsRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        # qs = SubmissionDb.objects.get(id=pk)
        qs = get_object_or_404(SubmissionDb,id=pk)
        serializer_instance = SubmissionSerializer(qs)
        return Response(data=serializer_instance.data)

    def delete(self,request,pk):
        SubmissionDb.objects.filter(id=pk).delete()
        return Response({"message":"Deleted!"})

    def put(self,request,pk):
        form_data = request.data
        serializer_instance = SubmissionSerializer(data=form_data)
        if serializer_instance.is_valid():
            org_data = serializer_instance.validated_data
            SubmissionDb.objects.filter(id=pk).update(**org_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class EvaluateSubmissionView(APIView):
    def put(self,request,pk):
        form_data = request.data
        SubmissionDb.objects.filter(id=pk).update(**form_data)
        return Response({"Message":"Updated!"})