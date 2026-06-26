#trekking_and_tour_management_system/packages/api/v1/serializers.py
from rest_framework import serializers

from rest_framework import serializers

from trekking_and_tour_management_system.packages.models import Category, TrekPackage
from trekking_and_tour_management_system.users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


class TrekPackageSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = TrekPackage
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "destination",
            "duration",
            "price",
            "guide_price",
            "difficulty",
            "description",
            "image",
            "featured",
            "available",
            "created_at",
        ]

class TrekPackageReadSerializer(
    serializers.ModelSerializer
):

    category = CategorySerializer()

    class Meta:
        model = TrekPackage
        fields = "__all__"

class TrekPackageWriteSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = TrekPackage

        fields = [
            "title",
            "category",
            "destination",
            "duration",
            "price",
            "guide_price",
            "difficulty",
            "description",
            "image",
            "featured",
            "available",
        ]