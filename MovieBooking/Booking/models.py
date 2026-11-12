from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MovieDb(models.Model):
    movie_name = models.CharField(max_length=200)

    def __str__(self):
        return self.movie_name

class ShowDb(models.Model):
    movie = models.ForeignKey(MovieDb,on_delete=models.CASCADE)
    show_date = models.DateField()
    show_time = models.TimeField()
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie_name} - {self.show_time}"

class BookingDb(models.Model):
    customer_name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=10)
    movie = models.ForeignKey(MovieDb,on_delete=models.CASCADE,related_name="movie_details")
    show = models.ForeignKey(ShowDb, on_delete=models.CASCADE,related_name="show_details")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_details")
    seats_booked = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','movie','show'],name="unique_booking")]

    def __str__(self):
        return f"{self.movie.movie_name}-{self.show.show_time}-{self.customer_name}"