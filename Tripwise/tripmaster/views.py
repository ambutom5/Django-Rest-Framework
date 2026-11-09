from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer, TripSerializer
from rest_framework import authentication, permissions
from tripmaster.models import TripDb

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


class UserListView(APIView):
    def get(self,request):
        qs = User.objects.all()
        serializer_instance = UserSerializer(qs, many=True)
        return Response(serializer_instance.data,status=200)


class TripListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        qs = TripDb.objects.all()
        serializer_instance = TripSerializer(qs, many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by = request.user)
            return Response({"Message":"Trip Created Successfully!",
                            "Trip Details":serializer_instance.data})
        else:
            return Response(serializer_instance.errors)


