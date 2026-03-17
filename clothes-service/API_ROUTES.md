# Clothes Service - API Routes

## Categories
- `GET /api/categories/` - Danh sách danh mục
- `POST /api/categories/` - Tạo danh mục mới (Admin)
- `PUT /api/categories/{id}/` - Cập nhật danh mục (Admin)
- `DELETE /api/categories/{id}/` - Xóa danh mục (Admin)

## Clothes (Products)
- `GET /api/clothes/` - Danh sách quần áo
- `POST /api/clothes/` - Tạo quần áo mới (Admin)
- `GET /api/clothes/{id}/` - Chi tiết quần áo
- `PUT /api/clothes/{id}/` - Cập nhật quần áo (Admin)
- `DELETE /api/clothes/{id}/` - Xóa quần áo (Admin)

## Filter & Search
- `GET /api/clothes/filter_by_category/?category_id=1` - Lọc theo danh mục
- `GET /api/clothes/filter_by_size/?size=M` - Lọc theo kích thước
- `GET /api/clothes/filter_by_color/?color=red` - Lọc theo màu
- `GET /api/clothes/search/?q=shirt` - Tìm kiếm
- `GET /api/clothes/top_rated/` - Quần áo được đánh giá cao
- `GET /api/clothes/on_sale/` - Quần áo đang khuyến mãi

## Reviews
- `GET /api/clothes/{id}/reviews/` - Danh sách đánh giá
- `POST /api/clothes/{id}/add_review/` - Thêm đánh giá mới
  ```json
  {
    "customer_id": 1,
    "customer_name": "Nguyễn Văn A",
    "rating": 5,
    "comment": "Quần áo rất tốt!"
  }
  ```

## Database Models

### Category
- id (Integer)
- name (String, unique)
- description (Text)
- created_at (DateTime)

### Clothes
- id (Integer)
- name (String)
- description (Text)
- price (Decimal)
- category_id (Foreign Key)
- size (Choice: XS, S, M, L, XL, XXL)
- color (Choice: red, blue, black, white, green, yellow, pink, brown, gray, purple)
- stock (Integer)
- image_url (URL)
- is_active (Boolean)
- rating (Float)
- created_at (DateTime)
- updated_at (DateTime)

### ClothesReview
- id (Integer)
- clothes_id (Foreign Key)
- customer_id (Integer)
- customer_name (String)
- rating (Integer: 1-5 stars)
- comment (Text)
- created_at (DateTime)
