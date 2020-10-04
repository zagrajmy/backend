from rest_framework import serializers

from crowd.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ["uuid", "email", "date_joined", "last_login"]
        fields = ["first_name", "last_name", "locale", "auth0_id", "username"]
        fields += read_only_fields
