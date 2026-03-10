# 📚 Bookstore Microservice

Hệ thống quản lý nhà sách xây dựng theo kiến trúc **Microservices** với Django REST Framework, giao tiếp qua API Gateway, giao diện web tích hợp sẵn.

---

## 🏗️ Kiến trúc hệ thống

```
                        ┌─────────────┐
                        │  Browser /  │
                        │   Client    │
                        └──────┬──────┘
                               │ :8000
                        ┌──────▼──────┐
                        │ API Gateway │  ← Web UI + Proxy
                        └──────┬──────┘
          ┌───────────┬────────┼────────┬───────────┐
          │           │        │        │           │
    ┌─────▼────┐ ┌────▼───┐ ┌─▼──────┐ ┌▼────────┐ ┌▼────────────┐
    │ customer │ │  book  │ │  cart  │ │  order  │ │    staff    │
    │  :8001   │ │ :8002  │ │ :8003  │ │  :8007  │ │   :8004     │
    └──────────┘ └────────┘ └────────┘ └─────────┘ └─────────────┘
          ┌──────────┬──────────┬────────────┬──────────┐
    ┌─────▼────┐ ┌───▼────┐ ┌──▼─────┐ ┌────▼───┐ ┌────▼──────────┐
    │ manager  │ │catalog │ │  ship  │ │  pay   │ │ comment-rate  │
    │  :8005   │ │ :8006  │ │ :8008  │ │ :8009  │ │    :8010      │
    └──────────┘ └────────┘ └────────┘ └────────┘ └───────────────┘
                                                   ┌───────────────┐
                                                   │ recommender-ai│
                                                   │    :8011      │
                                                   └───────────────┘
```

### Các service

| Service | Port | Chức năng |
|---------|------|-----------|
| **api-gateway** | 8000 | Web UI + điều phối request tới các service |
| **customer-service** | 8001 | Quản lý khách hàng, tự tạo giỏ hàng |
| **book-service** | 8002 | Quản lý sách, tồn kho |
| **cart-service** | 8003 | Giỏ hàng theo từng khách |
| **staff-service** | 8004 | Quản lý nhân viên |
| **manager-service** | 8005 | Quản lý quản lý/admin |
| **catalog-service** | 8006 | Danh mục, thể loại sách |
| **order-service** | 8007 | Đơn hàng + tự tạo payment & shipment |
| **ship-service** | 8008 | Vận chuyển |
| **pay-service** | 8009 | Thanh toán |
| **comment-rate-service** | 8010 | Đánh giá, bình luận |
| **recommender-ai-service** | 8011 | Gợi ý sách |

---

## ⚙️ Yêu cầu

| Công cụ | Phiên bản tối thiểu |
|---------|---------------------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | 24+ |
| [Docker Compose](https://docs.docker.com/compose/) | 2.20+ (tích hợp trong Docker Desktop) |

> **Không cần** cài Python, Django hay bất kỳ thư viện nào trực tiếp trên máy. Mọi thứ chạy trong container.

---

## 🚀 Cài đặt & Chạy

### 1. Clone dự án

```bash
git clone <repository-url>
cd bookstore-microservice
```

### 2. Build và khởi động toàn bộ hệ thống

```bash
docker compose up --build
```

Lần đầu sẽ mất **3–5 phút** để build 12 images. Các lần sau nhanh hơn.

Khi thấy dòng `Watching for file changes with StatReloader` xuất hiện cho tất cả service là đã sẵn sàng.

### 3. Truy cập

| URL | Mô tả |
|-----|-------|
| http://localhost:8000 | **Dashboard** — trang quản lý chính |
| http://localhost:8000/books/ | Quản lý sách |
| http://localhost:8000/customers/ | Quản lý khách hàng |
| http://localhost:8000/orders/ | Quản lý đơn hàng |
| http://localhost:8000/staff-page/ | Quản lý nhân viên |
| http://localhost:8000/payments-page/ | Lịch sử thanh toán |
| http://localhost:8000/shipments-page/ | Vận chuyển |
| http://localhost:8000/reviews-page/ | Đánh giá sách |
| http://localhost:8000/health/ | Kiểm tra trạng thái các service |

---

## 📡 API Endpoints

Tất cả request đi qua API Gateway theo pattern:

```
http://localhost:8000/api/<resource>/
http://localhost:8000/api/<resource>/<id>/
```

### Ví dụ

```bash
# Danh sách khách hàng
GET http://localhost:8000/api/customers/

# Tạo khách hàng mới (tự tạo giỏ hàng)
POST http://localhost:8000/api/customers/
Content-Type: application/json
{"name": "Nguyễn Văn A", "email": "a@example.com"}

# Xóa khách hàng
DELETE http://localhost:8000/api/customers/1/

# Danh sách sách
GET http://localhost:8000/api/books/

# Thêm sách
POST http://localhost:8000/api/books/
{"title": "Python Cơ Bản", "author": "Nguyễn B", "price": 150000, "stock": 10}

# Tạo đơn hàng có sản phẩm
POST http://localhost:8000/api/orders/
{
  "customer_id": 1,
  "shipping_address": "123 Nguyễn Huệ, Q1, HCM",
  "items": [
    {"book_id": 1, "quantity": 2, "unit_price": 150000},
    {"book_id": 3, "quantity": 1, "unit_price": 200000}
  ]
}
```

### Resources có sẵn

| Resource | Endpoint |
|----------|----------|
| customers | `/api/customers/` |
| books | `/api/books/` |
| carts | `/api/carts/` |
| staff | `/api/staff/` |
| managers | `/api/managers/` |
| categories | `/api/categories/` |
| orders | `/api/orders/` |
| shipments | `/api/shipments/` |
| payments | `/api/payments/` |
| reviews | `/api/reviews/` |
| recommendations | `/api/recommendations/` |

---

## 🛠️ Lệnh thường dùng

```bash
# Khởi động (background, không hiện log)
docker compose up -d

# Khởi động và xem log
docker compose up

# Dừng tất cả service
docker compose down

# Rebuild một service cụ thể (sau khi sửa code)
docker compose up --build -d api-gateway
docker compose up --build -d order-service

# Xem log một service
docker compose logs -f api-gateway
docker compose logs -f order-service

# Xem log tất cả
docker compose logs -f

# Kiểm tra trạng thái containers
docker compose ps

# Restart một service
docker compose restart api-gateway

# Xóa toàn bộ (kể cả dữ liệu)
docker compose down -v
```

---

## 📁 Cấu trúc thư mục

```
bookstore-microservice/
├── docker-compose.yml
├── api-gateway/
│   └── api_gateway/
│       ├── app/
│       │   └── views.py          # Proxy logic + template views
│       ├── templates/            # Giao diện web (HTML)
│       │   ├── base.html         # Layout chung (sidebar)
│       │   ├── dashboard.html
│       │   ├── books.html
│       │   ├── customers.html
│       │   ├── orders.html
│       │   ├── staff.html
│       │   ├── payments.html
│       │   ├── shipments.html
│       │   ├── reviews.html
│       │   └── cart.html
│       └── api_gateway/
│           └── urls.py
├── customer-service/
├── book-service/
├── cart-service/
├── staff-service/
├── manager-service/
├── catalog-service/
├── order-service/
├── ship-service/
├── pay-service/
├── comment-rate-service/
└── recommender-ai-service/
```
Mỗi service có cấu trúc Django chuẩn:
```
<name>-service/
├── Dockerfile
├── requirements.txt
└── <name>_service/
    ├── manage.py
    ├── app/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   └── migrations/
    └── <name>_service/
        ├── settings.py
        └── urls.py
```

---

## 🔄 Luồng hoạt động chính

### Tạo khách hàng
```
POST /api/customers/
    → customer-service: lưu Customer
    → customer-service: gọi cart-service tạo Cart tương ứng
```

### Tạo đơn hàng
```
POST /api/orders/
    → order-service: lưu Order + các OrderItem
    → order-service: gọi pay-service tạo Payment
    → order-service: gọi ship-service tạo Shipment
```

---

## ⚠️ Lưu ý

- **Dữ liệu** lưu trong SQLite bên trong mỗi container. Khi chạy `docker compose down -v` dữ liệu sẽ bị xóa.
- **Port 8000** phải trống trên máy host trước khi chạy.
- Nếu gặp lỗi port bị chiếm, đổi port trong `docker-compose.yml` (ví dụ `"8080:8000"`).
- Formatter/linter có thể phá vỡ cú pháp JavaScript template literal trong các file `.html` — các file template đã dùng string concatenation thay thế để tránh vấn đề này.

