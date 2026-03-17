from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Clothes, Category, ClothesReview
from .serializers import (
    ClothesSerializer,
    CategorySerializer,
    ClothesReviewSerializer,
    ClothesDetailSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet cho Danh mục quần áo"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ClothesViewSet(viewsets.ModelViewSet):
    """ViewSet cho Quần áo"""

    queryset = Clothes.objects.filter(is_active=True)
    serializer_class = ClothesSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClothesDetailSerializer
        return ClothesSerializer

    @action(detail=False, methods=["get"])
    def filter_by_category(self, request):
        """Lọc quần áo theo danh mục
        ?category_id=1
        """
        category_id = request.query_params.get("category_id")
        if not category_id:
            return Response(
                {"error": "category_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        clothes = Clothes.objects.filter(category_id=category_id, is_active=True)
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def filter_by_size(self, request):
        """Lọc quần áo theo kích thước
        ?size=M
        """
        size = request.query_params.get("size")
        if not size:
            return Response(
                {"error": "size is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        clothes = Clothes.objects.filter(size=size, is_active=True)
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def filter_by_color(self, request):
        """Lọc quần áo theo màu sắc
        ?color=red
        """
        color = request.query_params.get("color")
        if not color:
            return Response(
                {"error": "color is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        clothes = Clothes.objects.filter(color=color, is_active=True)
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Tìm kiếm quần áo
        ?q=shirt
        """
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response(
                {"error": "q (query) is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        clothes = Clothes.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query), is_active=True
        )
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_review(self, request, pk=None):
        """Thêm đánh giá cho quần áo"""
        clothes = self.get_object()
        serializer = ClothesReviewSerializer(data=request.data)
        serializer.initial_data["clothes_id"] = clothes.id

        if serializer.is_valid():
            serializer.save(clothes=clothes)

            # Cập nhật rating trung bình
            reviews = clothes.reviews.all()
            if reviews.exists():
                avg_rating = sum(review.rating for review in reviews) / reviews.count()
                clothes.rating = round(avg_rating, 1)
                clothes.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        """Lấy tất cả đánh giá của một quần áo"""
        clothes = self.get_object()
        reviews = clothes.reviews.all()
        serializer = ClothesReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top_rated(self, request):
        """Lấy những quần áo được đánh giá cao nhất"""
        limit = request.query_params.get("limit", 10)
        clothes = Clothes.objects.filter(is_active=True).order_by("-rating")[
            : int(limit)
        ]
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def on_sale(self, request):
        """Lấy quần áo đang khuyến mãi (stock > 5)"""
        clothes = Clothes.objects.filter(stock__gt=5, is_active=True).order_by(
            "-created_at"
        )
        serializer = self.get_serializer(clothes, many=True)
        return Response(serializer.data)


class ClothesReviewViewSet(viewsets.ModelViewSet):
    """ViewSet cho Đánh giá quần áo"""

    queryset = ClothesReview.objects.all()
    serializer_class = ClothesReviewSerializer
