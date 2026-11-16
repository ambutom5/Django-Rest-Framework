from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster.serializers import UserSerializer, TripSerializer, TripMemberSerializer
from rest_framework import authentication, permissions, serializers
from tripmaster.models import TripDb, TripMemberDb
from tripmaster import permissions as cpermissions
from rest_framework.exceptions import PermissionDenied

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

    def get(self,request,trip_id):
        # Get the trip
        trip_object = get_object_or_404(TripDb,id=trip_id)
        # 5, Trip to Munnar, Anas, ...

        is_owner = trip_object.created_by == request.user
        is_member = TripMemberDb.objects.filter(trip=trip_object,user=request.user).exists()

        if not (is_owner or is_member):
            raise PermissionDenied("You are not allowed to access this trip!")
        
        # Get all trip members
        members = TripMemberDb.objects.filter(trip=trip_object)
        serializer_instance = TripMemberSerializer(members,many=True)
        return Response(serializer_instance.data,status=200)
        

    def post(self,request,trip_id):
        trip_object = get_object_or_404(TripDb,id=trip_id)

        if trip_object.created_by != request.user:
            raise PermissionDenied("Only trip owner can add members!")
        
        form_data = request.data
        serializer_instance = TripMemberSerializer(data=form_data,context={'trip':trip_object})
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Member Added!","Data":serializer_instance.data})
        else:
            return Response(serializer_instance.errors,status =400)


class TripMemberDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request,trip_id,trip_member_id):
        trip_object = get_object_or_404(TripDb,id=trip_id)
        if trip_object.created_by != request.user:
            raise PermissionDenied("You are not allowed to remove members from this trip!")
        trip_member_object = TripMemberDb.objects.filter(id=trip_member_id)
        trip_member_object.delete()
        return Response({"Message":"Member Deleted!"})



