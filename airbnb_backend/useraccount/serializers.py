from rest_framework import serializers  # type: ignore

from .models import User  # type: ignore


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'avatar',
        )
