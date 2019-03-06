from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, default='')


class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='related_category_department')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, default='')


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2)
    discounted_price = models.DecimalField(decimal_places=2, default=0.00)
    image = models.ImageField()
    image_2 = models.ImageField()
    thumbnail = models.ImageField()
    display = models.SmallIntegerField(default=0)


class ProductCategory(models.Model):
    class Meta:
        unique_together = (('product', 'category'),)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='related_category')


class Attribute(models.Model):
    name = models.CharField(max_length=100)


class AttributeValue(models.Model):
    attribute = models.OneToOneField(Attribute, on_delete=models.CASCADE)
    pass


class ProductAttribute(models.Model):
    class Meta:
        unique_together = (('product', 'attribute_value'),)
    product = models.ForeignKey(Product)
    attribute_value = models.ForeignKey(AttributeValue)


class ShoppingCart(models.Model):
    cart_id = models.CharField(max_length=32)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    attributes = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    buy_now = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)


class Customer(AbstractUser):
    credit_card = models.TextField(null=True)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
   # shipping_region = models.ForeignKey(ShippingRegion)
    day_phone = models.CharField(max_length=100)
    eve_phone = models.CharField(max_length=100)
    mob_phone = models.CharField(max_length=100)
    pass


class Orders(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField()
    shipped_on = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=255)
    # customer_id = models.IntegerField()
    auth_code = models.CharField(max_length=50)
    reference = models.CharField(max_length=50)
    # shipping_id = models.
    # tax_id


class OrderDetail(models.Model):
    order = models.ForeignKey(Orders)
    product_id = models.IntegerField()
    attributes = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pass

class ShippingRegion(models.Model):
    shipping_region = models.CharField(max_length=100)


class Shipping(models.Model):
    shipping_type = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_region_id = models.ForeignKey(ShippingRegion)

class Tax(models.Model):
    tax_type = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)


class Audit(models.Model):
    order_id = models.ForeignKey(Orders)
    created_on = models.DateTimeField(blank=True, auto_now_add=True)
    message = models.TextField()
    code = models.IntegerField()


class ReviewTable(models.Model):
    customer_id = models.ForeignKey(Customer)
    product_id = models.ForeignKey(Product)
    review = models.TextField()
    rating = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
