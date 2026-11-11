from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Booking.models import TurfDb, BookingDb
from django.contrib.auth.models import User
from Booking.serializers import TurfSerializer, BookingSerializer, UserSerializer
from rest_framework import permissions, authentication, serializers
from Booking import permissions as cpermissions

# Create your views here.

class UserSignUpView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User Created Successfully!"},status=201)
        else:
            return Response(serializer_instance.errors,status=400)

class UserListView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        qs = User.objects.all()
        serializer_instance = UserSerializer(qs, many=True)
        return Response(serializer_instance.data)

class TurfListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        qs = TurfDb.objects.all()
        serializer_instance = TurfSerializer(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = TurfSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            # org_data = serializer_instance.validated_data
            # TurfDb.objects.create(**org_data)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class TurfRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request,pk):
        qs = get_object_or_404(TurfDb,id=pk)
        serializer_instance = TurfSerializer(qs)
        return Response(serializer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        qs = get_object_or_404(TurfDb,id=pk)
        serializer_instance = TurfSerializer(data=form_data,instance=qs)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

    def delete(self,request,pk):
        qs = get_object_or_404(TurfDb,id=pk)
        qs.delete()
        return Response({"Message":"Deleted!"})
    

class BookingListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        qs = BookingDb.objects.filter(created_by=request.user)
        # qs = BookingDb.objects.all()
        serializer_instance = BookingSerializer(qs,many=True)
        return Response(serializer_instance.data)
    
    def post(self,request):
        form_data = request.data
        serializer_instance = BookingSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class BookingRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated,cpermissions.OwnerOnly]

    def get(self,request,pk):
        qs = get_object_or_404(BookingDb,id=pk)
        self.check_object_permissions(request,qs)
        serializer_instance = BookingSerializer(qs)
        return Response(serializer_instance.data)

    def delete(self,request,pk):
        qs = get_object_or_404(BookingDb,id=pk)
        self.check_object_permissions(request,qs)
        qs.delete()
        return Response({"Message":"Booking Deleted!"})
        

    def put(self,request,pk):
        form_data = request.data
        qs = get_object_or_404(BookingDb,id=pk)
        self.check_object_permissions(request,qs)
        serializer_instance = BookingSerializer(data=form_data,instance=qs)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


