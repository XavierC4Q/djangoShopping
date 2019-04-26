from django.urls import path, include
from django.conf.urls import url
from .views import (
    UserViewSet,
    ProductViewSet,
    ProductDetailViewSet,
    OrderViewSet,
    HomeView,
    FootwearView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'user', UserViewSet, 'User')
router.register(r'product', ProductViewSet, 'Product')
router.register(r'productDetail', ProductDetailViewSet, 'Product Detail')
router.register(r'order', OrderViewSet, 'Order')

urlpatterns = [
    path('', include(router.urls)),
    url(r'^home/', HomeView, name='HomeView'),
    url(r'^footwear/', FootwearView, name='FootwearView'),
]