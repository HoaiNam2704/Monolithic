import os
import json as _json
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

SERVICES = {
    "customers": os.environ.get("CUSTOMER_SERVICE_URL", "http://customer-service:8000"),
    "books": os.environ.get("BOOK_SERVICE_URL", "http://book-service:8000"),
    "carts": os.environ.get("CART_SERVICE_URL", "http://cart-service:8000"),
    "staff": os.environ.get("STAFF_SERVICE_URL", "http://staff-service:8000"),
    "managers": os.environ.get("MANAGER_SERVICE_URL", "http://manager-service:8000"),
    "categories": os.environ.get("CATALOG_SERVICE_URL", "http://catalog-service:8000"),
    "orders": os.environ.get("ORDER_SERVICE_URL", "http://order-service:8000"),
    "shipments": os.environ.get("SHIP_SERVICE_URL", "http://ship-service:8000"),
    "payments": os.environ.get("PAY_SERVICE_URL", "http://pay-service:8000"),
    "reviews": os.environ.get(
        "COMMENT_RATE_SERVICE_URL", "http://comment-rate-service:8000"
    ),
    "recommendations": os.environ.get(
        "RECOMMENDER_SERVICE_URL", "http://recommender-ai-service:8000"
    ),
    "clothes": os.environ.get("CLOTHES_SERVICE_URL", "http://clothes-service:8000"),
}


#  Template Views


class RootView(APIView):
    def get(self, request):
        if not request.session.get("admin_manager_id"):
            return redirect("admin-login-page")
        return render(request, "dashboard.html")


def admin_login_page(request):
    if request.session.get("admin_manager_id"):
        return redirect("root")
    return render(request, "admin_login.html")


def admin_login_submit(request):
    if request.method != "POST":
        return redirect("admin-login-page")

    email = (request.POST.get("email") or "").strip().lower()
    employee_id = (request.POST.get("employee_id") or "").strip()
    if not email or not employee_id:
        return render(
            request,
            "admin_login.html",
            {
                "error": "Vui long nhap day du email va ma nhan vien.",
                "email": email,
                "employee_id": employee_id,
            },
        )

    try:
        resp = requests.get(f"{SERVICES['managers']}/managers/", timeout=6)
        managers = resp.json() if resp.ok else []
        managers = managers if isinstance(managers, list) else []
    except Exception:
        managers = []

    matched = None
    for m in managers:
        if (
            str(m.get("email", "")).strip().lower() == email
            and str(m.get("employee_id", "")).strip() == employee_id
            and bool(m.get("is_active", True))
        ):
            matched = m
            break

    if not matched:
        return render(
            request,
            "admin_login.html",
            {
                "error": "Thong tin admin khong dung hoac tai khoan da bi khoa.",
                "email": email,
                "employee_id": employee_id,
            },
        )

    request.session["admin_manager_id"] = matched.get("id")
    request.session["admin_name"] = matched.get("name", "Admin")
    request.session["admin_email"] = matched.get("email", email)
    request.session["admin_employee_id"] = matched.get("employee_id", employee_id)
    return redirect("root")


def admin_logout(request):
    for k in [
        "admin_manager_id",
        "admin_name",
        "admin_email",
        "admin_employee_id",
    ]:
        request.session.pop(k, None)
    return redirect("admin-login-page")


def _ensure_admin(request):
    if not request.session.get("admin_manager_id"):
        return redirect("admin-login-page")
    return None


def book_list(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    try:
        r = requests.get(f"{SERVICES['books']}/books/", timeout=5)
        books = r.json()
    except Exception:
        books = []
    return render(request, "books.html", {"books": books})


def customers_page(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    return render(request, "customers.html")


def orders_page(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    return render(request, "orders.html")


def staff_page(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    return render(request, "staff.html")


def payments_page(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    return render(request, "payments.html")


def shipments_page(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    return render(request, "shipments.html")


def reviews_page(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    return render(request, "reviews.html")


def clothes_page(request):
    guard = _ensure_admin(request)
    if guard:
        return guard
    try:
        r = requests.get(f"{SERVICES['clothes']}/api/clothes/", timeout=5)
        clothes = r.json()
        # Handle pagination
        if isinstance(clothes, dict) and "results" in clothes:
            clothes = clothes["results"]
    except Exception:
        clothes = []
    return render(request, "clothes.html", {"clothes": clothes})


def user_shop_page(request):
    user_id = request.session.get("user_customer_id")
    if not user_id:
        return redirect("user-login-page")
    return render(
        request,
        "shop.html",
        {
            "user_customer_id": user_id,
            "user_name": request.session.get("user_name", "Khach hang"),
            "user_email": request.session.get("user_email", ""),
        },
    )


def user_login_page(request):
    if request.session.get("user_customer_id"):
        return redirect("user-shop-page")
    return render(request, "user_login.html")


def user_register_page(request):
    if request.session.get("user_customer_id"):
        return redirect("user-shop-page")
    return render(request, "user_register.html")


def user_login_submit(request):
    if request.method != "POST":
        return redirect("user-login-page")

    email = (request.POST.get("email") or "").strip().lower()
    if not email:
        return render(
            request,
            "user_login.html",
            {"error": "Vui long nhap email.", "email": email},
        )

    try:
        resp = requests.get(f"{SERVICES['customers']}/customers/", timeout=6)
        customers = resp.json() if resp.ok else []
        customers = customers if isinstance(customers, list) else []
    except Exception:
        customers = []

    matched = None
    for c in customers:
        if str(c.get("email", "")).strip().lower() == email:
            matched = c
            break

    if not matched:
        return render(
            request,
            "user_login.html",
            {
                "error": "Email chua ton tai. Vui long dang ky tai khoan moi.",
                "email": email,
            },
        )

    request.session["user_customer_id"] = matched.get("id")
    request.session["user_name"] = matched.get("name", "Khach hang")
    request.session["user_email"] = matched.get("email", email)
    return redirect("user-shop-page")


def user_logout(request):
    for k in ["user_customer_id", "user_name", "user_email"]:
        request.session.pop(k, None)
    return redirect("user-login-page")


def user_register_submit(request):
    if request.method != "POST":
        return redirect("user-register-page")

    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip().lower()
    if not name or not email:
        return render(
            request,
            "user_register.html",
            {
                "error": "Vui long nhap day du ho ten va email.",
                "name": name,
                "email": email,
            },
        )

    try:
        check_resp = requests.get(f"{SERVICES['customers']}/customers/", timeout=6)
        customers = check_resp.json() if check_resp.ok else []
        customers = customers if isinstance(customers, list) else []
    except Exception:
        customers = []

    for c in customers:
        if str(c.get("email", "")).strip().lower() == email:
            return render(
                request,
                "user_register.html",
                {
                    "error": "Email da ton tai. Vui long dang nhap.",
                    "name": name,
                    "email": email,
                },
            )

    try:
        create_resp = requests.post(
            f"{SERVICES['customers']}/customers/",
            json={"name": name, "email": email},
            timeout=6,
        )
    except Exception:
        create_resp = None

    if not create_resp or not create_resp.ok:
        return render(
            request,
            "user_register.html",
            {
                "error": "Khong the tao tai khoan luc nay. Vui long thu lai.",
                "name": name,
                "email": email,
            },
        )

    created = create_resp.json()
    request.session["user_customer_id"] = created.get("id")
    request.session["user_name"] = created.get("name", name)
    request.session["user_email"] = created.get("email", email)
    return redirect("user-shop-page")


def view_cart(request, customer_id):
    try:
        r = requests.get(f"{SERVICES['carts']}/carts/{customer_id}/", timeout=5)
        data = r.json()
        items = data if isinstance(data, list) else data.get("items", [])
    except Exception:
        items = []
    return render(request, "cart.html", {"items": items, "customer_id": customer_id})


#  API Proxy


def _proxy(request, service_url, path):
    url = f"{service_url}/{path}"
    method = request.method.lower()
    body = None
    content_type = request.content_type or ""
    if request.body and "application/json" in content_type:
        try:
            body = _json.loads(request.body)
        except ValueError:
            body = None
    try:
        resp = getattr(requests, method)(url, json=body, params=request.GET, timeout=10)
        if resp.status_code == 204 or not resp.content:
            return JsonResponse({}, status=resp.status_code)
        try:
            return JsonResponse(resp.json(), status=resp.status_code, safe=False)
        except ValueError:
            return JsonResponse({}, status=resp.status_code)
    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {"error": f"Service unavailable: {service_url}"}, status=503
        )
    except requests.exceptions.Timeout:
        return JsonResponse({"error": "Service timeout"}, status=504)


class GatewayView(APIView):
    def dispatch(self, request, resource, path="", *args, **kwargs):
        if resource not in SERVICES:
            return Response(
                {"error": f"Unknown resource: {resource}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        base_url = SERVICES[resource]
        full_path = f"{resource}/{path}" if path else f"{resource}/"
        return _proxy(request, base_url, full_path)

    def get(self, request, resource, path=""):
        return self.dispatch(request, resource, path)

    def post(self, request, resource, path=""):
        return self.dispatch(request, resource, path)

    def put(self, request, resource, path=""):
        return self.dispatch(request, resource, path)

    def patch(self, request, resource, path=""):
        return self.dispatch(request, resource, path)

    def delete(self, request, resource, path=""):
        return self.dispatch(request, resource, path)


class HealthCheck(APIView):
    def get(self, request):
        results = {}
        for name, url in SERVICES.items():
            try:
                resp = requests.get(f"{url}/{name}/", timeout=3)
                results[name] = "up" if resp.status_code < 500 else "degraded"
            except requests.exceptions.RequestException:
                results[name] = "down"
        overall = "healthy" if all(v == "up" for v in results.values()) else "degraded"
        return Response({"status": overall, "services": results})
