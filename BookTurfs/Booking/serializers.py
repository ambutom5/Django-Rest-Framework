from rest_framework import serializers
from Booking.models import TurfDb, BookingDb
from datetime import datetime
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password","email"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfDb
        fields = "__all__"
        read_only_fields = ["id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDb
        fields = "__all__"
        read_only_fields = ["created_by"]

    def validate(self, validated_data):
        turf = validated_data.get("turf")
        booking_date = validated_data.get("booking_date")
        start_time = validated_data.get("start_time")
        end_time = validated_data.get("end_time")

        if booking_date < datetime.today().date():
            raise serializers.ValidationError("Booking Date Can't be Older Date")

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be greater than start time")

        overlapping_bookings = BookingDb.objects.filter(
            turf = turf,
            booking_date = booking_date,
            start_time__lt = end_time,
            end_time__gt = start_time)
        
        # Exclude the current booking during update
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Slot Not Available!")

        else:
            return validated_data



"""
How Slot Validation Works
Existing Start < New End AND Existing End > New Start

Existing Booking:
5 PM - 7 PM

New Booking:
6 PM - 8 PM

Check:
start_time__lt=end_time
5 PM < 8 PM ✅

and

end_time__gt=start_time
7 PM > 6 PM ✅

Both true ⇒ overlap found ⇒ booking rejected.
"""