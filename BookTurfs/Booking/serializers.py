from rest_framework import serializers
from Booking.models import TurfDb, BookingDb

class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfDb
        fields = "__all__"
        read_only_fields = ["id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDb
        fields = "__all__"
        read_only_fields = ["id"]