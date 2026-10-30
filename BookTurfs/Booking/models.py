from django.db import models

# Create your models here.

class TurfDb(models.Model):
    turf_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.turf_name

class BookingDb(models.Model):
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length = 15)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name