from Booking.models import MovieDb, ShowDb, BookingDb
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password","email"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


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


