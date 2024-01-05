from django.db import models
from django.conf import settings
from uuid import uuid4


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    @property
    def username(self):
        return self.user.username


    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.user.username


class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)


class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)


class Cryptocurrency(models.Model):
    CURRENCY_STATUS_WAITING = 'w'
    CURRENCY_STATUS_APPROVED = 'a'

    CURRENCY_STATUS =[
        (CURRENCY_STATUS_WAITING, 'Waiting'),
        (CURRENCY_STATUS_APPROVED, 'Approved'),
 
    ]
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cryptocurrenceis')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10 , decimal_places=6,null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to = 'covers/', blank = True)
    discounts = models.ManyToManyField(Discount, blank=True)
    status = models.CharField(choices=CURRENCY_STATUS, max_length=255, default=CURRENCY_STATUS_WAITING)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class MasterCart(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10 , decimal_places=6, null=True,blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to = 'covers/', blank = True)
    country = models.CharField()
    inventory = models.IntegerField()
    discounts = models.ManyToManyField(Discount, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class CommentCryptocurrency(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'

    COMMENT_STATUS =[
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
 
    ]
    user = models.ForeignKey(Customer , on_delete=models.CASCADE )
    cryptocurrency = models.ForeignKey(Cryptocurrency , on_delete=models.CASCADE , related_name='comments')
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=COMMENT_STATUS , max_length=50, default=COMMENT_STATUS_WAITING)


class CommentMasterCart(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'

    COMMENT_STATUS =[
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
 
    ]
    user = models.ForeignKey(Customer , on_delete=models.CASCADE )
    mastercart= models.ForeignKey(MasterCart, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=COMMENT_STATUS , max_length=50, default=COMMENT_STATUS_WAITING)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    datetime_created = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart= models.ForeignKey( Cart, on_delete=models.CASCADE , related_name='items')
    mastercart= models.ForeignKey(MasterCart , on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    cryptocurrency = models.ForeignKey(Cryptocurrency , on_delete=models.CASCADE, related_name='cart_items', null=True,blank=True)
    quantity_mastercart = models.PositiveIntegerField(null=True,blank=True)
    quantity_currency = models.PositiveIntegerField(null=True,blank=True)


class Order(models.Model):
    OREDR_STATUS_PAID = 'p'
    OREDR_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    
    ORDER_STATUS = [
        (OREDR_STATUS_PAID, 'Paid'),
        (OREDR_STATUS_UNPAID , 'UnPaid'),
        (ORDER_STATUS_CANCELED, 'Cancel'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS , max_length=10, default=OREDR_STATUS_UNPAID)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items')
    mastercart = models.ForeignKey(MasterCart, on_delete=models.CASCADE, related_name='order_items',null=True,blank=True)
    cryptocurrency = models.ForeignKey(Cryptocurrency , on_delete=models.CASCADE, related_name='order_items',null=True,blank=True)
    quantity_currency = models.PositiveIntegerField(null=True,blank=True)
    quantity_mastercart = models.PositiveIntegerField(null=True,blank=True)
    price_mastercart =models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    price_currency =models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)

