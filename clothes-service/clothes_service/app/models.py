from django.db import models


class Category(models.Model):
    """Danh mục quần áo"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Clothes(models.Model):
    """Mô hình quần áo"""

    SIZE_CHOICES = [
        ("XS", "Extra Small"),
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
        ("XXL", "XXL"),
    ]

    COLOR_CHOICES = [
        ("red", "Đỏ"),
        ("blue", "Xanh"),
        ("black", "Đen"),
        ("white", "Trắng"),
        ("green", "Xanh lá"),
        ("yellow", "Vàng"),
        ("pink", "Hồng"),
        ("brown", "Nâu"),
        ("gray", "Xám"),
        ("purple", "Tím"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="clothes"
    )
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    stock = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clothes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.size} - {self.color})"


class ClothesReview(models.Model):
    """Đánh giá quần áo"""

    clothes = models.ForeignKey(
        Clothes, on_delete=models.CASCADE, related_name="reviews"
    )
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100, default="Anonymous")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clothes_reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review cho {self.clothes.name} - {self.rating} stars"
