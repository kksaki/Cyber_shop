from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Cart(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product} - {self.quantity} - {self.created_date}"



# Create your models here.
class Product(models.Model):
    productNo = models.IntegerField()
    productName = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.TextField(null=True, blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    types = models.ForeignKey('Type', on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error saving product: {e}")

class Category(models.Model):
    id = models.TextField(primary_key=True)

    def __str__(self):
        return self.id

class Brand(models.Model):
    id = models.TextField(primary_key=True)

    def __str__(self):
        return self.id

class Type(models.Model):
    id = models.TextField(primary_key=True)

    def __str__(self):
        return self.id

    @classmethod
    def create_type(cls, type_id):
        try:
            type_obj, _ = cls.objects.get_or_create(id=type_id)
            return type_obj
        except Exception as e:
            print(f"Error creating type: {e}")
            return None

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    username = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username},{self.first_name}, {self.first_name}, {self.email},{self.created_date}'

    class Meta:
        db_table = 'customer'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
            try:
                instance.customer.save()
            except Customer.DoesNotExist:
                Customer.objects.create(user=instance)
    post_save.connect(save_user_profile, sender=User)


class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        try:
            return sum(item.get_cost() for item in self.items.all())
        except:
            return "Unable to calculate total cost"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        try:
            cost = self.price * self.quantity
        except TypeError:
            cost = 0
        return cost

class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
                   validators=[MinValueValidator(0),
                               MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


