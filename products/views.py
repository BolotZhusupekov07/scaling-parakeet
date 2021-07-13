from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Comment, Product, Variation
from .serializer import (ProductSerializer,
                         CommentSerializer,
                         VariationSerializer)
from carts.models import Cart
from orders.models import Order


class APIHomeView(APIView):
    def get(self, request, format=None):
        data = {
            "authentication": {
                "register": reverse("register_api", request=request),
                "login": reverse("login_api", request=request),
                "token_refresh":reverse("token_refresh", request=request)
            },
            "products": {
                "count": Product.objects.all().count(),
                "url": reverse("products_api", request=request),
            },
            "product_variations": {
                "count": Variation.objects.all().count(),
                "url": reverse("variations_api", request=request),
            },
            "comments": {
                "count": Comment.objects.all().count(),
                "url": reverse("comments_api", request=request),
            },
            "carts": {
                "count": Cart.objects.all().count(),
                "url": reverse("carts_api", request=request),
                "Here you add the product to your cart":reverse("add_to_cart_api",
                                                                request=request)
            },
            "orders": {
                "count": Order.objects.all().count(),
                "url": reverse("orders_api", request=request),
            },
            "checkout":{
                "message":"Here you can make a purchase",
                "url": reverse("checkout_api", request=request)
            }
        }
        return Response(data)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class VariationList(generics.ListCreateAPIView):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer


class VariationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer