from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MovieDb(models.Model):
    movie_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.movie_name

class ShowDb(models.Model):
    movie = models.ForeignKey(MovieDb,on_delete=models.CASCADE,related_name="shows")
    show_date = models.DateField()
    show_time = models.TimeField()
    # Theatre capacity
    total_seats = models.PositiveIntegerField()
    # Current seats available
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.movie_name} - {self.show_time}"

class BookingDb(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings")
    show = models.ForeignKey(ShowDb, on_delete=models.CASCADE,related_name="bookings")
    seats_booked = models.PositiveIntegerField()
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','show'],name="unique_booking")]

    def __str__(self):
        return f"{self.show.movie.movie_name}-{self.show.show_time}-{self.user.username}"

        #   Everything about the customer comes from User, and everything about the movie comes through:
        #   booking.show.movie.movie_name
        #   So you wouldn't even need the separate movie foreign key either.