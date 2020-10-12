from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ["date_joined", "last_login", "uuid"]
        fields = ["auth0_id", "email", "first_name", "last_name", "locale", "username"]
        fields += read_only_fields
