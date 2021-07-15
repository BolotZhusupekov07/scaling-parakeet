from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)



class OrderDetailAPI(generics.RetrieveAPIView):

    serializer_class = OrderSerializer
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        if order.user != request.user:
            raise PermissionDenied("You cannnot view other people's orders")
        serializer = self.serializer_class(order)
        return Response(serializer.data)