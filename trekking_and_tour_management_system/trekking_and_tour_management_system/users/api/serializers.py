from rest_framework import serializers
from trekking_and_tour_management_system.users.models import User, TrekPackage


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "role",
        ]
        read_only_fields = ["role"]

class TrekPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrekPackage
        fields = [
            "id",
            "name",
            "description",
            "price",
            "available",
        ]   