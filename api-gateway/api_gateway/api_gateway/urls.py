"""
URL configuration for api_gateway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from app.views import (
    GatewayView,
    HealthCheck,
    RootView,
    admin_login_page,
    admin_login_submit,
    admin_logout,
    book_list,
    clothes_page,
    user_login_page,
    user_login_submit,
    user_register_page,
    user_register_submit,
    user_logout,
    user_shop_page,
    view_cart,
    customers_page,
    orders_page,
    staff_page,
    payments_page,
    shipments_page,
    reviews_page,
)

urlpatterns = [
    path("admin/login/", admin_login_page, name="admin-login-page"),
    path("admin/login/submit/", admin_login_submit, name="admin-login-submit"),
    path("admin/logout/", admin_logout, name="admin-logout"),
    path("", RootView.as_view(), name="root"),
    path("user/login/", user_login_page, name="user-login-page"),
    path("user/login/submit/", user_login_submit, name="user-login-submit"),
    path("user/register/", user_register_page, name="user-register-page"),
    path("user/register/submit/", user_register_submit, name="user-register-submit"),
    path("user/logout/", user_logout, name="user-logout"),
    path("shop/", user_shop_page, name="user-shop-page"),
    path("health/", HealthCheck.as_view(), name="health-check"),
    # Template pages
    path("books/", book_list, name="book-list"),
    path("clothes/", clothes_page, name="clothes-page"),
    path("customers/", customers_page, name="customers-page"),
    path("orders/", orders_page, name="orders-page"),
    path("staff-page/", staff_page, name="staff-page"),
    path("payments-page/", payments_page, name="payments-page"),
    path("shipments-page/", shipments_page, name="shipments-page"),
    path("reviews-page/", reviews_page, name="reviews-page"),
    path("cart/<int:customer_id>/", view_cart, name="view-cart"),
    re_path(
        r"^api/(?P<resource>[\w-]+)/(?P<path>.*)$",
        GatewayView.as_view(),
        name="gateway",
    ),
]
