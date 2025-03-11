from django.contrib import admin  # type: ignore
from .models import Property, Reservation

admin.site.register(Property)
admin.site.register(Reservation)
