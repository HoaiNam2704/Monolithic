from rest_framework import serializers
from .models import Clothes, Category, ClothesReview


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at"]


class ClothesReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesReview
        fields = [
            "id",
            "clothes_id",
            "customer_id",
            "customer_name",
            "rating",
            "comment",
            "created_at",
        ]


class ClothesSerializer(serializers.ModelSerializer):
    reviews = ClothesReviewSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Clothes
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "category_name",
            "size",
            "color",
            "stock",
            "image_url",
            "is_active",
            "rating",
            "review_count",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_review_count(self, obj):
        return obj.reviews.count()


class ClothesDetailSerializer(serializers.ModelSerializer):
    reviews = ClothesReviewSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    review_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Clothes
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "category_name",
            "size",
            "color",
            "stock",
            "image_url",
            "is_active",
            "rating",
            "review_count",
            "avg_rating",
            "reviews",
            "created_at",
            "updated_at",
        ]

    def get_review_count(self, obj):
        return obj.reviews.count()

    def get_avg_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            avg = sum(review.rating for review in reviews) / reviews.count()
            return round(avg, 1)
        return 0.0
