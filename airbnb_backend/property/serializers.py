from rest_framework import serializers  # type: ignore

from .models import Property, Reservation
from useraccount.serializers import UserDetailSerializer


class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
        )


class PropertiesDetailSerializer(serializers.ModelSerializer):
    host = UserDetailSerializer(read_only=True, many=False)

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'host',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'country_code',
            'category',
            'image_url',
        )


class ReservationListSerializer(serializers.ModelSerializer):
    property = PropertiesListSerializer(read_only=True, many=False)

    class Meta:
        model = Reservation
        fields = (
            'id', 'start_date', 'end_date', 'number_of_nights', 'guests', 'total_price', 'property'
        )
