from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Booking.models import TurfDb, BookingDb
from django.contrib.auth.models import User
from Booking.serializers import TurfSerializer, BookingSerializer,UserSerializer

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

class TurfListCreateView(APIView):
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
    def get(self,request):
        qs = BookingDb.objects.all()
        serializer_instance = BookingSerializer(qs,many=True)
        return Response(serializer_instance.data)
    
    def post(self,request):
        form_data = request.data
        serializer_instance = BookingSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class BookingRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = get_object_or_404(BookingDb,id=pk)
        serializer_instance = BookingSerializer(qs)
        return Response(serializer_instance.data)

    def delete(self,request,pk):
        qs = get_object_or_404(BookingDb,id=pk)
        qs.delete()

    def put(self,request,pk):
        form_data = request.data
        qs = get_object_or_404(BookingDb,id=pk)
        serializer_instance = BookingSerializer(data=form_data,instance=qs)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


