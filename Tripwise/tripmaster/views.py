from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer, TripSerializer, TripMemberSerializer
from rest_framework import authentication, permissions, serializers
from tripmaster.models import TripDb, TripMemberDb
from tripmaster import permissions as cpermissions

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
        qs = TripDb.objects.filter(created_by = request.user)
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


class TripRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated,cpermissions.OwnerOnly]

    def get(self,request,pk):
        qs = get_object_or_404(TripDb,id=pk)
        self.check_object_permissions(request,qs)
        serializer_instance = TripSerializer(qs)
        return Response(serializer_instance.data)


    def put(self,request,pk):
        qs = get_object_or_404(TripDb,id=pk)
        self.check_object_permissions(request,qs)
        form_data = request.data
        serializer_instance = TripSerializer(qs,data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


    def delete(self,request,pk):
        qs = get_object_or_404(TripDb,id=pk)
        self.check_object_permissions(request,qs)
        qs.delete()
        return Response({"Message":"Trip Deleted!"})


class TripMemberListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        qs = TripMemberDb.objects.all()
        self.check_object_permissions(request,qs)
        serializer_instance = TripMemberSerializer(qs)
        return Response(serializer_instance.data)


    def post(self,request,pk):
        form_data = request.data
        serializer_instance = TripMemberSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)





