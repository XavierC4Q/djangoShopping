from .models import (
    User,
    Product,
    ProductDetail,
    Order
)
from .serializers import (
    UserSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    OrderSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
import requests as req


API = 'http://localhost:8000/app/'

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @action(detail=False, methods=['GET'])
    def category(self, request):
        cat = request.GET.get('category', '')
        res = Product.objects.filter(product_type__iexact=cat)
        serializer = self.get_serializer(res, many=True)

        return Response(serializer.data)


class ProductDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ProductDetailSerializer
    queryset = ProductDetail.objects.all()

    @action(detail=False, methods=['GET'])
    def sub_category(self, request):
        sub_cat = request.GET.get('sub_category', '')
        res = ProductDetail.objects.filter(sub_category__iexact=sub_cat)
        serializer = self.get_serializer(res, many=True)

        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


def HomeView(request):
    return render(request, 'app/home.html')

def FootwearView(request):
    path = f'{API}product/category/?category=footwear'
    try:
        get_footwear = req.get(path)
        data = get_footwear.json()
        context = {
            'title': 'Footwear',
            'items': data
        }
        return render(request, 'app/product-view.html', context)
    except:
        return render(request, 'app/home.html', context={'message': 'Failed to get Footwear'})
