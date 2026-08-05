from rest_framework import serializers
from .models import User
from sheets.models import ProfileModel


class UserSerializer(serializers.ModelSerializer):
    profiles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ProfileModel.objects.all())

    class Meta:
        model = User
        fields = ["id", "username", "profiles"]
