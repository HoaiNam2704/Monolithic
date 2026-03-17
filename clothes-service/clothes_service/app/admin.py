from django.contrib import admin
from .models import Category, Clothes, ClothesReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "size",
        "color",
        "price",
        "stock",
        "rating",
        "is_active",
        "created_at",
    ]
    list_filter = ["category", "size", "color", "is_active", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["rating", "created_at", "updated_at"]

    fieldsets = (
        ("Thông tin cơ bản", {"fields": ("name", "description", "category")}),
        ("Chi tiết sản phẩm", {"fields": ("size", "color", "price", "stock")}),
        (
            "Metadata",
            {
                "fields": (
                    "image_url",
                    "rating",
                    "is_active",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ClothesReview)
class ClothesReviewAdmin(admin.ModelAdmin):
    list_display = ["clothes", "customer_name", "rating", "created_at"]
    list_filter = ["rating", "created_at"]
    search_fields = ["clothes__name", "customer_name", "comment"]
    readonly_fields = ["created_at"]
