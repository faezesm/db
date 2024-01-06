from django.shortcuts import render
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import status



from . models import Cryptocurrency, Customer, MasterCart, CommentCryptocurrency, CommentMasterCart, Cart , CartItem
from . serializers import CryptocurrencySerializer, MasterCartSerializer, AddCommentCryptocurrencySerializer, CommentMasterCartSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,ChangeCartItemSerializer,AddCurrencySerilaizer,CommentCryptocurrencySerializer,CommentMasterCartSerializer,AddCommentMasterCartSerializer,ForAdminCurrencySerilaizer,ForAdminCommentCryptocurrencySerializer,ForAdminMasterCartSerializer,ForAdminCommentMasterCartSerializer,CustomerSerializer
from . permissions import IsAdminOrReadOnly,IsOwnerOrReadOnly


class CustomerViewSet(ModelViewSet):
    http_method_names = ['get','put','patch']
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]


    @action(detail=False, methods=['GET','PUT','PATCH'], permission_classes =[IsAuthenticated])
    def me(self , request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id = user_id)
        if request.method =='GET':
            serializer = CustomerSerializer(customer)
            return Response({
            'username': serializer.data['username'],
            'password': serializer.data['password'],
            'is_staff': serializer.data['is_staff'],}, status=status.HTTP_200_OK )

        elif request.method in ['PUT','PATCH']:
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        

class CryptocurrencyViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method in ['PATCH','PUT','DELETE']:
            return [IsAdminUser()]
        
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Cryptocurrency.objects.select_related('user__user').all()
        return Cryptocurrency.objects.select_related('user__user').filter(status='a').all()
    
 

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCurrencySerilaizer
        if self.request.method in ['PATCH','PUT']:
            return ForAdminCurrencySerilaizer
        return CryptocurrencySerializer

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
    @action(detail=False,methods=["GET",'DELETE'], permission_classes =[IsAuthenticated])
    def me(self , request):
        user_id = request.user.id
        queryset = Cryptocurrency.objects.filter(user_id =user_id)
        customer = Customer.objects.get(user_id = user_id)

        if request.method =='GET':
            serializer = CryptocurrencySerializer(queryset, many=True)
            return Response(serializer.data)


class CommentCryptocurrencyViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method in ['PATCH','PUT']:
            return [IsAdminUser()]
        
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CommentCryptocurrency.objects.all()
        return CommentCryptocurrency.objects.filter(status='a')


    def get_serializer_class(self):
        if self.request.method in ['PUT',"PATCH"]:
            return ForAdminCommentCryptocurrencySerializer
        if self.request.method == 'GET':
            return CommentCryptocurrencySerializer
        if self.request.method == 'POST':
            return AddCommentCryptocurrencySerializer


    def get_serializer_context(self):
        return {'currency_pk':self.kwargs['currency_pk'],
                        'user_id':self.request.user.id,
        }

    
class MasterCartViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method in ['PATCH','PUT','POST','DELETE']:
            return [IsAdminUser()]
        
        return [IsAuthenticated()]

    def get_queryset(self):
            return MasterCart.objects.all()



    def get_serializer_class(self):
        if self.request.method in ['PUT',"PATCH",'POST']:
            return ForAdminMasterCartSerializer
        if self.request.method == 'GET':
            return MasterCartSerializer



class CommentMasterCartViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method in ['PATCH','PUT']:
            return [IsAdminUser()]
        
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CommentMasterCart.objects.all()
        return CommentMasterCart.objects.filter(status='a')

    def get_serializer_class(self):
        if self.request.method in ['PUT',"PATCH"]:
            return ForAdminCommentMasterCartSerializer
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
    permission_classes=[AllowAny]
    serializer_class =CartSerializer
    
    def get_queryset(self):
        return Cart.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=CartItem.objects.select_related('mastercart').select_related('cryptocurrency')
            )
        )
    
class CartItemViewSet(ModelViewSet):
    permission_classes=[AllowAny]
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
    



