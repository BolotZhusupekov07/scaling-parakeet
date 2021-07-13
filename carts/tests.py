from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from decimal import Decimal


from users.models import NewUser
from products.models import Product, Category, Variation
from carts.models import Cart, CartItem
from .views import AddProductToCartAPI, CheckoutAPIView
from .models import CartItemCheckout
from .serializer import CartItemSerializer, CartSerializer



factory = APIRequestFactory()


class CartViews(TestCase):
    def setUp(self) -> None:
        supplier = NewUser.objects.create_user(email='supplier@gmail.com',role=1, password='kirgizia' )
        user = NewUser.objects.create_user(email='bolot.jusupekovv@gmail.com',role=2, password='kirgizia')
        category = Category.objects.create(name='books')
        product = Product.objects.create(title='Think, and Grow Rich',
                               description='book',
                               price='20.10',
                               discount=10,
                               supplier=supplier,
                               category=category
                               )
        product_variation = Variation.objects.create(product=product,
                                 title='Think, and Grow Rich',
                                 price='20.10',
                                 discount=10,
        )
        cart = Cart.objects.get(user=supplier)
        # for checkout view
        CartItem.objects.create(cart=cart, product=product_variation, quantity=3)
    def test_add_product_to_cart(self):
        
        request = factory.post('/api/carts/add_product/',
                            {"user": "bolot.jusupekovv@gmail.com",
                            "product":"Think, and Grow Rich / 20.10 / 10 %",
                            "quantity":4}, format='json')
        
        response = AddProductToCartAPI.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message":"Successfully added to the cart"}) 
        # +1 for checkout testing
        self.assertEqual(CartItem.objects.all().count(), 2)

        
    def test_checkout(self):
                        
        request = factory.post('/api/carts/checkout/',
                                {"user":"supplier@gmail.com"},
                                format='json')
        response = CheckoutAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItemCheckout.objects.all().count(),1)
        self.assertEqual(CartItem.objects.all().count(), 0)


class TestCartSerializers(APITestCase):
    def setUp(self) -> None:
        supplier = NewUser.objects.create_user(email='supplier@gmail.com',role=1, password='kirgizia' )
        category = Category.objects.create(name='books')
        product = Product.objects.create(title='Think, and Grow Rich',
                               description='book',
                               price='20.10',
                               discount=10,
                               supplier=supplier,
                               category=category
                               )
        product_variation = Variation.objects.create(product=product,
                                 title='Think, and Grow Rich',
                                 price='20.10',
                                 discount=10,
        )
        cart = Cart.objects.get(user=supplier)


        self.cartitem = CartItem.objects.create(cart=cart, product=product_variation, quantity=3)
        self.cartitem_serializer = CartItemSerializer(instance=self.cartitem)

        # add more one product to a cart
        product_2 = Product.objects.create(title='Django for Beginners',
                               description='programming book',
                               price='16.78',
                               discount=8,
                               supplier=supplier,
                               category=category
                               )
        product_variation_2 = Variation.objects.create(product=product,
                                 title='Django for Beginners',
                                 price='16.78',
                                 discount=8,
        )
        self.cartitem2 = CartItem.objects.create(cart=cart, product=product_variation_2, quantity=4)
        print(CartItem.objects.all().count())
        self.cart_serializer = CartSerializer(instance=cart)
    def test_cartitem_serializer(self):
        #20.10 * 3 = 60.3
        self.assertEqual(Decimal(self.cartitem_serializer['total_price'].value),Decimal("60.30"))
        # - discount 
        self.assertEqual(Decimal(self.cartitem_serializer['total_price_with_discount'].value),Decimal("54.27"))

    def test_cart_serializer(self):
        # 60.30 + (16.78 * 4) = 127.42
        
        self.assertEqual(Decimal(self.cart_serializer['total_price'].value), Decimal('127.42'))

        # 54.27 + (16.78 - (16.78*8)/100) = 116.0204
        self.assertEqual(Decimal(self.cart_serializer['total_price_with_discount'].value), Decimal(
            '116.0204'
        ))