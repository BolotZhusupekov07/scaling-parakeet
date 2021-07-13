from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from products.views import (
    APIHomeView,
    ProductList,
    ProductDetail,
    CommentList,
    CommentDetail,
    VariationList,
    VariationDetail
)
from carts.views import (
    CartAPIView,
    CartDetailAPIView,
    AddProductToCartAPI,
    CheckoutAPIView,
)

from users.views import (
    RegisterView,
    VerifyEmailView,
    LoginView,
)
from orders.views import (
    OrderListAPI,
    OrderDetailAPI
) 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", APIHomeView.as_view(),
         name="home_api"),
    path("api/register/", RegisterView.as_view(),
         name="register_api"),
    path("api/register/email_verify/", VerifyEmailView.as_view(),
         name="email_verify"),
    path("api/login/", LoginView.as_view(),
         name="login_api"),
    path("api/token/refresh/", TokenRefreshView.as_view(),
         name="token_refresh"),
    path("api/carts/", CartAPIView.as_view(),
         name="carts_api"),
    path("api/carts/add_product/", AddProductToCartAPI.as_view(),
         name="add_to_cart_api"),
    path("api/carts/<int:pk>", CartDetailAPIView.as_view(),
         name="cart_api_detail"),
    path("api/orders/", OrderListAPI.as_view(),
         name="orders_api"),
    path("api/orders/<int:pk>", OrderDetailAPI.as_view(),
         name="order_detail_api"),
    path("api/checkout/", CheckoutAPIView.as_view(),
         name="checkout_api"),
    path("api/products/", ProductList.as_view(),
         name="products_api"),
    path("api/products/<int:pk>", ProductDetail.as_view(),
         name="product_api_detail"),
    path("api/products/comments/", CommentList.as_view(),
         name="comments_api"),
    path(
        "api/products/comments/<int:pk>",
        CommentDetail.as_view(),
        name="comment_api_detail",
    ),
    path("api/products/variations/", VariationList.as_view(),
         name="variations_api"),
    path(
        "api/products/variations/<int:pk>",
        VariationDetail.as_view(),
        name="variation_api_detail",
    )
]
