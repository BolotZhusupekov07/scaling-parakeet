from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from decimal import Decimal


from users.models import NewUser
from products.models import Product, Category, Variation
from carts.models import Cart, CartItem
from orders.views import OrderListAPI, OrderDetailAPI, GetPriceWithPromocode
from orders.models import Promocode, Order
from .views import AddProductToCartAPI, CheckoutAPIView, CartAPIView
from .models import CartItemCheckout
from .serializer import CartItemSerializer, CartSerializer


factory = APIRequestFactory()


class CartViews(TestCase):
    def setUp(self) -> None:
        supplier = NewUser.objects.create_user(
            email="supplier@gmail.com", role=1, password="kirgizia"
        )
        user = NewUser.objects.create_user(
            email="bolot.jusupekovv@gmail.com", role=2, password="kirgizia"
        )
        category = Category.objects.create(name="books")
        product = Product.objects.create(
            title="Think, and Grow Rich",
            description="book",
            price="20.10",
            discount=10,
            supplier=supplier,
            category=category,
        )
        product_variation = Variation.objects.create(
            product=product,
            title="Think, and Grow Rich",
            price="20.10",
            discount=10,
        )
        cart = Cart.objects.get(user=user)
        # for checkout view
        CartItem.objects.create(cart=cart, product=product_variation, quantity=3)
        Promocode.objects.create(name="django", discount=25)

    def test_get_cart(self):
        user = NewUser.objects.get(email="bolot.jusupekovv@gmail.com")
        request = factory.get("/api/cart/")
        force_authenticate(request, user=user)
        response = CartAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_product_to_cart(self):
        user = NewUser.objects.get(email="bolot.jusupekovv@gmail.com")
        request = factory.post(
            "/api/cart/add_product/",
            {"product": "Think, and Grow Rich / 20.10 / 10 %", "quantity": 4},
            format="json",
        )
        force_authenticate(request, user=user)
        response = AddProductToCartAPI.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Successfully added to the cart"})
        # +1 for checkout testing
        self.assertEqual(CartItem.objects.all().count(), 2)

    def test_checkout_and_many_more(self):
        user = NewUser.objects.get(email="bolot.jusupekovv@gmail.com")
        supplier = NewUser.objects.get(email="supplier@gmail.com")
        request = factory.post("/api/cart/checkout/", format="json")
        force_authenticate(request, user=user)
        response = CheckoutAPIView.as_view()(request)

        request2 = factory.get("/api/orders/")
        force_authenticate(request2, user=user)
        response2 = OrderListAPI.as_view()(request2)

        request3 = factory.get("/api/orders/1/")
        force_authenticate(request3, user=user)
        response3 = OrderDetailAPI.as_view()(request3, pk=1)

        request4 = factory.get("/api/checkout/django/")
        force_authenticate(request4, user=user)
        response4 = GetPriceWithPromocode.as_view()(request4, promocode="django")

        request5 = factory.get("/api/orders/2/")
        force_authenticate(request5, user=user)
        response5 = OrderDetailAPI.as_view()(request5, pk=2)

        request6 = factory.get("/api/checkout/react/")
        force_authenticate(request6, user=user)
        response6 = GetPriceWithPromocode.as_view()(request6, promocode="react")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response6.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(CartItemCheckout.objects.all().count(), 1)
        self.assertEqual(CartItem.objects.all().count(), 0)


class TestCartSerializers(APITestCase):
    def setUp(self) -> None:
        supplier = NewUser.objects.create_user(
            email="supplier@gmail.com", role=1, password="kirgizia"
        )
        category = Category.objects.create(name="books")
        product = Product.objects.create(
            title="Think, and Grow Rich",
            description="book",
            price="20.10",
            discount=10,
            supplier=supplier,
            category=category,
        )
        product_variation = Variation.objects.create(
            product=product,
            title="Think, and Grow Rich",
            price="20.10",
            discount=10,
        )
        cart = Cart.objects.get(user=supplier)

        self.cartitem = CartItem.objects.create(
            cart=cart, product=product_variation, quantity=3
        )
        self.cartitem_serializer = CartItemSerializer(instance=self.cartitem)

        # add more one product to a cart
        product_2 = Product.objects.create(
            title="Django for Beginners",
            description="programming book",
            price="16.78",
            discount=8,
            supplier=supplier,
            category=category,
        )
        product_variation_2 = Variation.objects.create(
            product=product,
            title="Django for Beginners",
            price="16.78",
            discount=8,
        )
        self.cartitem2 = CartItem.objects.create(
            cart=cart, product=product_variation_2, quantity=4
        )
        print(CartItem.objects.all().count())
        self.cart_serializer = CartSerializer(instance=cart)

    def test_cartitem_serializer(self):
        # 20.10 * 3 = 60.3
        self.assertEqual(
            Decimal(self.cartitem_serializer["total_price"].value), Decimal("60.30")
        )
        # - discount
        self.assertEqual(
            Decimal(self.cartitem_serializer["total_price_with_discount"].value),
            Decimal("54.27"),
        )

    def test_cart_serializer(self):
        # 60.30 + (16.78 * 4) = 127.42

        self.assertEqual(
            Decimal(self.cart_serializer["total_price"].value), Decimal("127.42")
        )

        # 54.27 + (16.78 - (16.78*8)/100) = 116.0204
        self.assertEqual(
            Decimal(self.cart_serializer["total_price_with_discount"].value),
            Decimal("116.0204"),
        )
