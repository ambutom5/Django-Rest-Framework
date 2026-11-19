from Booking.models import MovieDb, ShowDb, BookingDb
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id","username","password","email"]

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

    def create(self,validated_data):
        validated_data["available_seats"] = validated_data["total_seats"]
        return ShowDb.objects.create(**validated_data)

class BookingSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source="show.movie.movie_name",read_only=True)
    show_time = serializers.TimeField(source="show.show_time",read_only=True)

    class Meta:
        model = BookingDb
        fields = "__all__"
        read_only_fields = ["id","user","booked_at"]


    def validate(self, validated_data):
        user = self.context["request"].user
        # DRF removes read-only fields(user) from validated_data.
        show = validated_data["show"]
        seats_booked = validated_data["seats_booked"]

        if seats_booked > show.available_seats:
            raise serializers.ValidationError("Not enough seats available!")
        
        qs = BookingDb.objects.filter(user=user,show=show)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("You already have a booking for this show!")
        return validated_data
    

    def create(self,validated_data):
        show = validated_data["show"]
        seats_booked = validated_data["seats_booked"]
        show.available_seats -= seats_booked
        show.save()
        return BookingDb.objects.create(user=self.context["request"].user,**validated_data)
    

    def update(self,instance,validated_data):
        new_seats = validated_data["seats_booked"]
        old_seats = instance.seats_booked
        difference = new_seats - old_seats

        if difference > instance.show.available_seats:
            raise serializers.ValidationError("Not enough seats available!")

        instance.show.available_seats -= difference
        instance.show.save()

        instance.seats_booked = new_seats
        instance.save()

        return instance



