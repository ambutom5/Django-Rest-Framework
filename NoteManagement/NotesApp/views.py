from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import serializers
from NotesApp.serializers import RegisterSerializer, NotesSerializer
from NotesApp.models import NotesDb
from rest_framework.permissions import IsAuthenticated

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


class NotesListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        notes = NotesDb.objects.filter(user=request.user)
        serializer_instance = NotesSerializer(notes,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        serializer_instance = NotesSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


class NotesRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        qs = get_object_or_404(NotesDb,id=pk,user=request.user)
        serializer_instance = NotesSerializer(qs)
        return Response(serializer_instance.data)

    def delete(self,request,pk):
        qs = get_object_or_404(NotesDb,id=pk,user=request.user)
        qs.delete()
        return Response({"Message":"Note Deleted"})

    def put(self,request,pk):
        qs = get_object_or_404(NotesDb,id=pk,user=request.user)
        serializer_instance = NotesSerializer(qs,data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)