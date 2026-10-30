from rest_framework import serializers
from clinic.models import DoctorDb,AppointmentDb
from datetime import datetime
from django.utils import timezone

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDb
        fields = "__all__"
        # fields = ["id", "doctor_name","specialization",]
        read_only_fields = ["id"]

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDb
        fields = "__all__"
        read_only_fields = ["id"]

    def validate(self,validated_data):
        phone = validated_data.get("phone")
        appointment_date = validated_data.get("appointment_date")
        # if appointment_date < datetime.today().date():
        if appointment_date < timezone.localdate():
            raise serializers.ValidationError("Invalid Date!")
        if AppointmentDb.objects.filter(phone=phone,appointment_date=appointment_date).exists():
            raise serializers.ValidationError("Already booked!")
        else:
            return validated_data


# ModelSerializer
# Default field generation
# Default Validation
# Conversion between model instances and serialized data
# class Meta: Defines the serializer's configuration