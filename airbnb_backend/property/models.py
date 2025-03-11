import uuid

from django.conf import settings  # type: ignore
from django.db import models  # type: ignore

from useraccount.models import User


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()

    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()

    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=10)
    category = models.CharField(max_length=255)

    image = models.ImageField(upload_to='uploads/properties/')
    host = models.ForeignKey(
        User, related_name='properties', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def image_url(self):
        return f'{settings.WEBSITE_URL}{self.image.url}'


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(
        Property, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guests = models.IntegerField(default=1)
    total_price = models.FloatField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
