from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import serializers
from NotesApp.serializers import RegisterSerializer


# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = RegisterSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User Registered Successfully", "Details":serializer_instance.data})
        else:
            return Response(serializer_instance.errors)

class UserListView(APIView):
    def get(self,request):
        qs = User.objects.all()
        serializer_instance = RegisterSerializer(qs,many=True)
        return Response(serializer_instance.data)
