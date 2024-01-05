from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('currencies', views.CryptocurrencyViewSet , basename = 'currency')
router.register('mastercarts', views.MasterCartViewSet , basename='mastercart')
router.register('carts', views.CartViewSet, basename='cart')



currency_router = routers.NestedDefaultRouter(router, 'currencies', lookup = 'currency')
currency_router.register('comments', views.CommentCryptocurrencyViewSet , basename='comment')

mastercart_router = routers.NestedDefaultRouter(router, 'mastercarts',lookup = 'mastercart')
mastercart_router.register('comments', views.CommentMasterCartViewSet, basename='comment')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart_item')


urlpatterns = [
   path('',include(router.urls+currency_router.urls+ mastercart_router.urls+cart_router.urls)),
]
