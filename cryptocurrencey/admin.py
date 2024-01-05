from django.contrib import admin

from .models import Cryptocurrency, Customer, CommentCryptocurrency, MasterCart,CommentMasterCart,Cart , CartItem


class CommentCrptocurrencyInLine(admin.TabularInline):
        model = CommentCryptocurrency
        fields =['user', 'body','status']
        extra =1


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'title','price','datetime_created']
    inlines=[CommentCrptocurrencyInLine]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['user','full_name' ,'username']

class CommentMasterCartInLine(admin.TabularInline):
    model= CommentMasterCart
    fields=['user', 'body','status']
    extra =1

@admin.register(MasterCart)
class MasterCartAdmin(admin.ModelAdmin):
    list_display=['id','title','price','description','country','image','inventory']
    inlines=[CommentMasterCartInLine]

class CartItemInLine(admin.TabularInline):
    model = CartItem
    fields= ['cryptocurrency','quantity_currency','mastercart','quantity_mastercart']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','datetime_created']
    inlines = [CartItemInLine]






