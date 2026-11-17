from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Booking.models import MovieDb, ShowDb, BookingDb
from Booking.serializers import MovieSerializer, ShowSerializer, BookingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import authentication, permissions


# Create your views here.

class UserSignUpView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializer(data =form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User Created Successfully!"},status=201)
        else:
            return Response({"Message":"Invalid Details!"},status=400)


class UserListView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        qs = User.objects.all()
        serializer_instance = UserSerializer(qs,many=True)
        return Response(serializer_instance.data)

    

class MovieListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        qs = MovieDb.objects.all()
        serializer_instance = MovieSerializer(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = MovieSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class MovieRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request,pk):
        qs = get_object_or_404(MovieDb,id=pk)
        serializer_instance = MovieSerializer(qs)
        return Response(serializer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        qs = get_object_or_404(MovieDb, id=pk)
        serializer_instance = MovieSerializer(data=form_data,instance=qs)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

    def delete(self,request,pk):
        qs = get_object_or_404(MovieDb, id=pk)
        qs.delete()
        return Response({"Message":"Deleted!"})


class ShowListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request):
        qs = ShowDb.objects.all()
        serializer_instance = ShowSerializer(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = ShowSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)


class ShowRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self,request,pk):
        qs = get_object_or_404(ShowDb,id=pk)
        serializer_instance = ShowSerializer(qs)
        return Response(serializer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        qs = get_object_or_404(ShowDb,id=pk)
        serializer_instance = ShowSerializer(qs,data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

    def delete(self,request,pk):
        qs = get_object_or_404(ShowDb,id=pk)
        qs.delete()
        return Response({"Message":"Deleted!"})


class ShowListView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        qs = ShowDb.objects.all()
        serializer_instance = ShowSerializer(qs,many=True)
        return Response(serializer_instance.data)


class BookingListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        qs = BookingDb.objects.filter(user=request.user)
        serializer_instance = BookingSerializer(qs,many=True)
        return Response(serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance=BookingSerializer(data=form_data,context={"request":request})
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Booked Successfully!","Details":serializer_instance.data},status=201)
        else:
            return Response(serializer_instance.errors,status=400)


class BookingRetriveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        qs = get_object_or_404(BookingDb,id=pk,user=request.user)
        serializer_instance = BookingSerializer(qs)
        return Response(serializer_instance.data)

    def delete(self,request,pk):
        qs = get_object_or_404(BookingDb,id=pk,user=request.user)
        qs.delete()
        return Response({"Message":"Booking Deleted!"})

    def put(self,request,pk):
        qs = get_object_or_404(BookingDb,id=pk,user=request.user)
        form_data = request.data
        serializer_instance = BookingSerializer(data=form_data,instance=qs,context={"request":request})
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Booking Updated Successfully!","Details":serializer_instance.data},status=201)
        else:
            return Response(serializer_instance.errors,status=400)
