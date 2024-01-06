from rest_framework import serializers
from django.contrib.auth import get_user_model

from . models import Cryptocurrency,Customer, MasterCart, CommentCryptocurrency,CommentMasterCart, Cart, CartItem

class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length = 255 , source='user.full_name')
    username = serializers.CharField(max_length = 255 , source='user.username')
    password = serializers.CharField(max_length = 255 , source='user.password')
    is_staff = serializers.CharField(max_length = 255 , source='user.is_staff')
    class Meta:
        model = Customer
        fields = ['id','full_name','username','password','is_staff']
        read_only_fields =['user']



class ForAdminCurrencySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields =['id', 'user','title','price','image','description','status', 'datetime_created']
        read_only_fields =['user']
    
    def create(self, validate_data):
        user_id = self.context['user_id']
        cryptocurrency = Cryptocurrency.objects.create(user_id=user_id, **validate_data)
        return cryptocurrency

class AddCurrencySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields =['id', 'user','title','price','image','description', 'datetime_created']
        read_only_fields =['user']
    
    def create(self, validate_data):
        user_id = self.context['user_id']
        cryptocurrency = Cryptocurrency.objects.create(user_id=user_id, **validate_data)
        return cryptocurrency

class CustomerCryptocurrency(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, source='user.full_name',read_only=True)
    class Meta:
        model = Customer
        fields = ['full_name']

    
class CryptocurrencySerializer(serializers.ModelSerializer):
    user = CustomerCryptocurrency()
    class Meta:
        model = Cryptocurrency
        fields = ['id', 'user','title','price','image','description','status','datetime_created']

class ForAdminMasterCartSerializer(serializers.ModelSerializer):
     class Meta:
        model = MasterCart
        fields = ['id','title','price','image','description','country', 'inventory','datetime_created']

class MasterCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterCart
        fields = ['id','title','price','image','description','country', 'inventory','datetime_created']

class ForAdminCommentCryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentCryptocurrency
        fields = ['id','user','body','status','datetime_created']
        read_only_fields =['user']

    def create(self, validated_data):
        user_id = self.context['user_id']
        currency_id = self.context['currency_pk']
        return CommentCryptocurrency.objects.create(cryptocurrency_id = currency_id,user_id =user_id, **validated_data)


class CommentCryptocurrencySerializer(serializers.ModelSerializer):
    user = CustomerCryptocurrency()
    class Meta:
        model = CommentCryptocurrency
        fields = ['id','user','body','status','datetime_created']


class AddCommentCryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentCryptocurrency
        fields = ['id','user','body', 'datetime_created']
        read_only_fields =['user']

    def create(self, validated_data):
        user_id = self.context['user_id']
        currency_id = self.context['currency_pk']
        return CommentCryptocurrency.objects.create(cryptocurrency_id = currency_id,user_id =user_id, **validated_data)


class ForAdminCommentMasterCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMasterCart
        fields = ['id','user','body','status', 'datetime_created']
        read_only_fields =['user']
    
    def create(self , validate_data):
        user_id = self.context['user_id']
        mastercart_id = self.context['mastercart_pk']
        return CommentMasterCart.objects.create(mastercart_id= mastercart_id , user_id= user_id , **validate_data)


class CommentMasterCartSerializer(serializers.ModelSerializer):
    user = CustomerCryptocurrency()
    class Meta:
        model = CommentMasterCart
        fields = ['id','user','body','status', 'datetime_created']


class  AddCommentMasterCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMasterCart
        fields = ['id','user','body', 'datetime_created']
        read_only_fields =['user']
    
    def create(self , validate_data):
        user_id = self.context['user_id']
        mastercart_id = self.context['mastercart_pk']
        return CommentMasterCart.objects.create(mastercart_id= mastercart_id , user_id= user_id , **validate_data)

class MasterCartCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterCart
        fields =['title','price','image']

class CurrencyCartItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = Cryptocurrency
        fields =['title','price','image']

class ItemCartItemSerializer(serializers.ModelSerializer):
    mastercart= MasterCartCartItemSerializer()
    cryptocurrency =CurrencyCartItemSerializer()
    class Meta :
        model = CartItem
        fields =['cryptocurrency','quantity_currency','mastercart','quantity_mastercart']

class CartSerializer(serializers.ModelSerializer):
    items =ItemCartItemSerializer(many=True, read_only=True)
    class Meta:
        model =Cart
        fields =['id','items']
        read_only_fields =['id']


class ChangeCartItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = CartItem
        fields =['quantity_mastercart','quantity_currency']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields =['mastercart', 'quantity_mastercart','cryptocurrency', 'quantity_currency']


    def create(self , validate_data):
        cart_pk = self.context['cart_pk']

        currency = validate_data.get('cryptocurrency')
        mastercart = validate_data.get('mastercart')
        quantity_mastercart = validate_data.get('quantity_mastercart')
        quantity_currency = validate_data.get('quantity_currency')
        if (currency and  quantity_currency) == None :
            try :
                cart_item = CartItem.objects.get(cart_id = cart_pk,  mastercart_id=mastercart.id)
                cart_item.quantity_mastercart += quantity_mastercart
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(cart_id = cart_pk, **validate_data)
            return cart_item

        if (mastercart and  quantity_mastercart) == None :
            try :
                cart_item = CartItem.objects.get(cart_id = cart_pk,  cryptocurrency_id= currency.id)
                cart_item.quantity_currency += quantity_currency
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(cart_id = cart_pk, **validate_data)
            return cart_item
        else :
            try :
                cart_item = CartItem.objects.get(cart_id = cart_pk,  cryptocurrency_id= currency.id, mastercart_id = mastercart.id)
                cart_item.quantity_currency += quantity_currency
                cart_item.quantity_mastercart += quantity_mastercart
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(cart_id = cart_pk, **validate_data)
            return cart_item


class CartItemSerializer(serializers.ModelSerializer):
    mastercart =MasterCartCartItemSerializer(read_only=True)
    cryptocurrency=CurrencyCartItemSerializer(read_only=True)
    total_price_mastercart = serializers.SerializerMethodField()
    total_price_currency = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['mastercart','quantity_mastercart','total_price_mastercart','cryptocurrency','quantity_currency','total_price_currency']

    def get_total_price_mastercart(self , cart_item:CartItem):
        if cart_item.mastercart== None:
            return
        return cart_item.quantity_mastercart * cart_item.mastercart.price

    def get_total_price_currency(self , cartitem):
        if cartitem.cryptocurrency== None:
            return
        return cartitem.quantity_currency * cartitem.cryptocurrency.price








    
