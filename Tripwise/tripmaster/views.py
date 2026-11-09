from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer

# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User Created Successfully!"}, status=201)
        else:
            return Response({"Message":"Invalid Data Provided!"}, status=400)
