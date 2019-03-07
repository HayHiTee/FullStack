from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, default='')


class Category(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='related_category_department')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, default='')


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10,decimal_places=2, default=0.00)
    image = models.ImageField()
    image_2 = models.ImageField()
    thumbnail = models.ImageField()
    display = models.SmallIntegerField(default=0)


class ProductCategory(models.Model):
    class Meta:
        unique_together = (('product_id', 'category_id'),)
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='related_product')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='related_category')


class Attribute(models.Model):
    name = models.CharField(max_length=100)


class AttributeValue(models.Model):
    attribute_id = models.ForeignKey(Attribute, on_delete=models.CASCADE,
                                     related_name='attribute_value_related_attribute')
    value = models.CharField(max_length=100)
    pass


class ProductAttribute(models.Model):
    class Meta:
        unique_together = (('product_id', 'attribute_value_id'),)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attribute_related_product')
    attribute_value_id = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,
                                           related_name='product_attribute_related_attribute_value')


class ShoppingCart(models.Model):
    cart_id = models.CharField(max_length=32)
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    attributes = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    buy_now = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)


class ShippingRegion(models.Model):
    shipping_region = models.CharField(max_length=100)


class Customer(AbstractUser):
    credit_card = models.TextField(null=True)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    shipping_region_id = models.ForeignKey(ShippingRegion,
                                           on_delete=models.CASCADE, related_name='customer_related_shipping_region')
    day_phone = models.CharField(max_length=100)
    eve_phone = models.CharField(max_length=100)
    mob_phone = models.CharField(max_length=100)
    pass


class Shipping(models.Model):
    shipping_type = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_region_id = models.ForeignKey(ShippingRegion,
                                           on_delete=models.CASCADE, related_name='shipping_related_region')


class Tax(models.Model):
    tax_type = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)


class Orders(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField()
    shipped_on = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=255, null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders_related_customer')
    auth_code = models.CharField(max_length=50, null=True)
    reference = models.CharField(max_length=50, null=True)
    shipping_id = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='orders_related_shipping')
    tax_id = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='orders_related_tax')


class OrderDetail(models.Model):
    order = models.ForeignKey(Orders, on_delete='order_detail_related_order')
    product_id = models.IntegerField()
    attributes = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pass


class Audit(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='audit_related_order')
    created_on = models.DateTimeField(blank=True, auto_now_add=True)
    message = models.TextField()
    code = models.IntegerField()


class ReviewTable(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='review_table_related_customer')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_table_related_product')
    review = models.TextField()
    rating = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
