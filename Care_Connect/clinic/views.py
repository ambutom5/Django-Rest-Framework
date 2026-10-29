from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DoctorDb,AppointmentDb
from clinic.serializers import DoctorSerializer,AppointmentSerializer
from datetime import time,timedelta,datetime
from rest_framework import serializers


# Create your views here.

class DoctorListCreateView(APIView):
    def get(self,request):
        qs = DoctorDb.objects.all()
        serializer_instance = DoctorSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serialaizer_instance = DoctorSerializer(data=form_data)
        if serialaizer_instance.is_valid():
            serialaizer_instance.save()
            return Response(data=serialaizer_instance.data)
        else:
            return Response(serialaizer_instance.errors)


class DoctorRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = get_object_or_404(DoctorDb,id=pk)
        serilizer_instance = DoctorSerializer(qs)
        return Response(data=serilizer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        doctor_object = get_object_or_404(DoctorDb,id=pk)
        serializer_instance = DoctorSerializer(data = form_data, instance = doctor_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data= serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

    def delete(self,request,pk):
        doctor_object = get_object_or_404(DoctorDb,id=pk)
        doctor_object.delete()
        return Response(data={"Message":"Deleted!"})


class AppointmentListCreateView(APIView):
    def get(self,request):
        qs = AppointmentDb.objects.all()
        serializer_instance = AppointmentSerializer(qs,many=True)
        return Response(data = serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = AppointmentSerializer(data=form_data)
        if serializer_instance.is_valid():
            print(serializer_instance.validated_data)
            appointment_date = serializer_instance.validated_data.get("appointment_date")
            doctor_id = serializer_instance.validated_data.get("doctor_id")

            last_appointment = AppointmentDb.objects.filter(
                appointment_date = appointment_date,
                doctor_id = doctor_id
            ).order_by("-token_number").first()
            
            # print(last_appointment)
            # print(last_appointment.__dict__)

            if last_appointment is None:
                form_data["token_number"] = 1
                form_data["appointment_time"] = time(10,0)
                
            else:
                form_data["token_number"] = last_appointment.token_number + 1
                current_time = datetime.combine(appointment_date,last_appointment.appointment_time)
                next_time = current_time + timedelta(minutes=15)
                
                # Adding Lunch Break
                if next_time.time() == time(12,30):
                    next_time = datetime.combine(appointment_date,time(13,30))

                if next_time.time() == time(18,00):
                    raise serializers.ValidationError("Booking Closed!")

                form_data["appointment_time"] = next_time.time()
                        
                       
            qs = AppointmentDb.objects.create(**form_data)
            serializer_instance = AppointmentSerializer(qs)
            return Response(data={"Message" : "Booked Successfully!",
                "Token Number is " : form_data["token_number"],
                "Appointment Date is" : form_data["appointment_date"],
                "Appointment Time is" : form_data["appointment_time"]
                })
        else:
            return Response(serializer_instance.errors)
