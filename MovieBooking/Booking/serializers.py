from Booking.models import MovieDb, ShowDb, BookingDb
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDb
        fields = "__all__"
        read_only_fields = ["id"]

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowDb
        fields = "__all__"
        read_only_fields = ["id"] 

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDb
        fields = "__all__"
        read_only_fields = ["id"]


