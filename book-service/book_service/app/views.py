from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookListCreate(APIView):
    """
    APIView hỗ trợ:
    - GET: Lấy toàn bộ danh sách sách.
    - POST: Thêm một cuốn sách mới vào kho.
    """

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        # Trả về dữ liệu kèm mã 200 OK (mặc định)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Trả về dữ liệu mới tạo kèm mã 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Nếu dữ liệu không hợp lệ, trả về lỗi kèm mã 400 Bad Request
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)