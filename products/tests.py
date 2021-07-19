from django.test import TestCase
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory, APITestCase
from .models import Category, Product, Variation, Comment, Reply
from .permissions import IsAuthorOrReadOnly, IsOwner, IsSupplier
from users.models import NewUser
from .views import ProductDetail, ProductList, APIHomeView, CommentList, RepliesList

factory = APIRequestFactory()


class TestProductModels(APITestCase):
    def test_models_str(self):
        category = Category.objects.create(name="books")
        self.assertEqual(str(category), "books")
        supplier = NewUser.objects.create(
            email="supplier@gmail.com", role=1, password="password"
        )
        client = NewUser.objects.create(
            email="client@gmail.com", role=2, password="password"
        )
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
        self.assertEqual(str(product), "Think, and Grow Rich / 20.10")
        self.assertEqual(str(product_variation), "Think, and Grow Rich / 20.10 / 10 % ")
        comment = Comment.objects.create(
            product=product, author=client, content="I love it", rate=4
        )
        self.assertEqual(str(comment), "I love it")


class TestProductViews(APITestCase):
    def setUp(self):
        self.supplier = NewUser.objects.create_superuser(
            email="supplier@gmail.com", role=1, password="password"
        )
        self.client = NewUser.objects.create_user(
            email="client@gmail.com", role=2, password="password"
        )

        self.category = Category.objects.create(name="books")
        self.product = Product.objects.create(
            title="Think, and Grow Rich",
            description="book",
            price="20.10",
            discount=10,
            supplier=self.supplier,
            category=self.category,
        )
        self.comment = Comment.objects.create(
            product=self.product, content="Comment Content", rate=4, author=self.client
        )
        self.reply = Reply.objects.create(
            comment=self.comment, content="Reply Content", rate=5, author=self.supplier
        )

    def test_product_get_views(self):
        user = NewUser.objects.get(email="supplier@gmail.com")
        request = factory.get("/api/products/")
        force_authenticate(request, user=user)
        response = ProductList.as_view()(request)

        request2 = factory.get("/api/")
        force_authenticate(request2, user=user)
        response2 = APIHomeView.as_view()(request2)

        request3 = factory.get("/api/products/comments/")
        force_authenticate(request3, user=user)
        response3 = CommentList.as_view()(request3)

        request4 = factory.get("/api/products/comments/replies/")
        force_authenticate(request4, user=user)
        response4 = RepliesList.as_view()(request4)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)

    def test_product_post_views(self):
        user = NewUser.objects.get(email="supplier@gmail.com")
        user2 = NewUser.objects.get(email="client@gmail.com")
        data = {
            "title": "Book Title",
            "description": "Book Desc",
            "pictures": [
                {"image_url": "media/images/test.png"},
                {"image_url": "media/images/test2.png"},
            ],
            "price": "14.56",
            "discount": 15,
            "category": {"name": "books"},
        }

        data_2 = {
            "title": "Book Title",
            "description": "Book Desc",
            "pictures": [
                {"image_url": "media/images/test.png"},
                {"image_url": "media/images/test2.png"},
            ],
            "price": "14.56",
            "discount": 15,
            "category": 1,
        }
        request = factory.post("/api/products/", data, format="json")
        request_2 = factory.post("/api/products/", data_2, format="json")
        force_authenticate(request, user=user)
        force_authenticate(request_2, user=user)
        response = ProductList.as_view()(request)
        response_2 = ProductList.as_view()(request_2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

        data2 = {"product": self.product.id, "rate": 4, "content": "comment content"}
        data2_1 = {"product": 1, "rate": 4, "content": "comment content"}
        request2 = factory.post("/api/products/comments/", data2, format="json")
        request2_1 = factory.post("/api/products/comments/", data2_1, format="json")
        force_authenticate(request2, user=user2)
        force_authenticate(request2_1, user=user2)
        response2 = CommentList.as_view()(request2)
        response2_1 = CommentList.as_view()(request2_1)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2_1.status_code, status.HTTP_400_BAD_REQUEST)

        data3 = {"comment": self.comment.id, "content": "reply content", "rate": 2}
        data3_1 = {"comment": 1, "content": "reply content", "rate": 2}
        request3 = factory.post("/api/products/comments/replies/", data3, format="json")
        request3_1 = factory.post(
            "/api/products/comments/replies/", data3_1, format="json"
        )
        force_authenticate(request3, user=user2)
        force_authenticate(request3_1, user=user2)
        response3 = RepliesList.as_view()(request3)
        response3_1 = RepliesList.as_view()(request3_1)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3_1.status_code, status.HTTP_400_BAD_REQUEST)
