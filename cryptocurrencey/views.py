from django.shortcuts import render
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins



from . models import Cryptocurrency, Customer, MasterCart, CommentCryptocurrency, CommentMasterCart, Cart , CartItem
from . serializers import CryptocurrencySerializer, MasterCartSerializer, AddCommentCryptocurrencySerializer, CommentMasterCartSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,ChangeCartItemSerializer,AddCurrencySerilaizer,CommentCryptocurrencySerializer,CommentMasterCartSerializer,AddCommentMasterCartSerializer
from . permissions import IsAdminOrReadOnly

class CryptocurrencyViewSet(ModelViewSet):
    queryset = Cryptocurrency.objects.select_related('user__user').filter(status='a')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CryptocurrencySerializer
        if self.request.method == 'POST':
            return AddCurrencySerilaizer

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
    @action(detail=False,methods=["GET"], permission_classes =[IsAuthenticated])
    def me(self , request):
        user_id = request.user.id
        queryset = Cryptocurrency.objects.filter(user_id =user_id)
        customer = Customer.objects.get(user_id = user_id)

        if request.method =='GET':
            serializer = CryptocurrencySerializer(queryset, many=True)
            return Response(serializer.data)


class CommentCryptocurrencyViewSet(ModelViewSet):
    queryset = CommentCryptocurrency.objects.filter(status='a')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentCryptocurrencySerializer
        if self.request.method == 'POST':
            return AddCommentCryptocurrencySerializer


    def get_serializer_context(self):
        return {'currency_pk':self.kwargs['currency_pk'],
                        'user_id':self.request.user.id,
        }

    
class MasterCartViewSet(ModelViewSet):
    serializer_class = MasterCartSerializer
    queryset = MasterCart.objects.all()
    permission_classes=[IsAdminOrReadOnly]


class CommentMasterCartViewSet(ModelViewSet):
    queryset = CommentMasterCart.objects.filter(status='a')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentMasterCartSerializer
        if self.request.method == 'POST':
            return AddCommentMasterCartSerializer

    def get_serializer_context(self):
        return {'mastercart_pk':self.kwargs['mastercart_pk'],
                        'user_id':self.request.user.id,
          }

class CartViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class =CartSerializer
    
    def get_queryset(self):
        return Cart.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=CartItem.objects.select_related('mastercart').select_related('cryptocurrency')
            )
        )
    
class CartItemViewSet(ModelViewSet):
    http_method_names=['get', 'patch', 'post', 'delete']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer 
        
        if self.request.method == 'PATCH':
            return ChangeCartItemSerializer
        return CartItemSerializer

    def  get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related('mastercart').select_related('cryptocurrency').filter(cart_id = cart_pk)
        

    def get_serializer_context(self):
        return {'cart_pk':self.kwargs['cart_pk']}
    



