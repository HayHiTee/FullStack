from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=50)
    is_customer = models.BooleanField(default=True)


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, default='')


class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='related_category_department')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField()
    image_2 = models.ImageField()
    thumbnail = models.ImageField()
    display = models.SmallIntegerField(default=0)

    def get_categories_string(self):
        categories = ''
        qs = self.related_product.all()
        for q in qs:
            categories += '{} '.format(q.category)
        print(categories)
        return categories

    def get_default_size(self):
        sizes = AttributeValue.objects.filter(attribute_id=1)[0]
        prod_attr = self.product_attribute_related_product.filter(attribute_value=sizes)[0]
        return prod_attr.attribute_value

    def get_default_colour(self):
        colors = AttributeValue.objects.filter(attribute_id=2)[0]
        prod_attr = self.product_attribute_related_product.filter(attribute_value=colors)[0]

        return prod_attr.attribute_value


class ProductCategory(models.Model):
    class Meta:
        unique_together = (('product', 'category'),)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='related_category')


class Attribute(models.Model):
    name = models.CharField(max_length=100)


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,
                                     related_name='attribute_value_related_attribute')
    value = models.CharField(max_length=100)
    pass


class ProductAttribute(models.Model):
    class Meta:
        unique_together = (('product', 'attribute_value'),)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attribute_related_product')
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,
                                           related_name='product_attribute_related_attribute_value')

class ShoppingCart(models.Model):
    cart_id = models.CharField(max_length=32)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    attributes = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    buy_now = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)


class ShippingRegion(models.Model):
    shipping_region = models.CharField(max_length=100)

    def __str__(self):
        return  self.shipping_region


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    credit_card = models.TextField(null=True)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    shipping_region = models.ForeignKey(ShippingRegion,
                                           on_delete=models.CASCADE, related_name='customer_related_shipping_region')
    day_phone = models.CharField(max_length=100)
    eve_phone = models.CharField(max_length=100)
    mob_phone = models.CharField(max_length=100)
    pass


class Shipping(models.Model):
    shipping_type = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_region = models.ForeignKey(ShippingRegion,
                                           on_delete=models.CASCADE, related_name='shipping_related_region')


class Tax(models.Model):
    tax_type = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "{} {}".format(self.tax_type, self.tax_percentage)


class Orders(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField()
    shipped_on = models.DateTimeField(null=True)
    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders_related_customer')
    auth_code = models.CharField(max_length=50, null=True)
    reference = models.CharField(max_length=50, null=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='orders_related_shipping')
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='orders_related_tax')


class OrderDetail(models.Model):
    order = models.ForeignKey(Orders, on_delete='order_detail_related_order')
    product = models.ForeignKey(Product, on_delete='order_detail_related_product')
    attributes = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    pass


class Audit(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='audit_related_order')
    created_on = models.DateTimeField(blank=True, auto_now_add=True)
    message = models.TextField()
    code = models.IntegerField()


class ReviewTable(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='review_table_related_customer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_table_related_product')
    review = models.TextField()
    rating = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
