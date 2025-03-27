from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User


def non_empty(value):
    if not value.strip():
        raise serializers.ValidationError("Це поле не може бути порожнім.")
    return value


def validate_full_name(value):
    words = value.strip().split()
    if len(words) < 2:
        raise serializers.ValidationError(
            "Ім'я має складатися з двох слів (ім'я та прізвище).")
    return value


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(
        required=True, max_length=255, validators=[non_empty, validate_full_name]
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['name'] = self.validated_data.get('name', '')
        return data

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.save(update_fields=['name'])


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'avatar_url',
        )
