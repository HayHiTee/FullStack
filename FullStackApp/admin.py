from django.contrib import admin

#Admin Dashboard

# Register your models here.
from FullStackApp.models import User, Product, Customer, Orders, OrderDetail, ShippingRegion, Shipping, Attribute, \
    AttributeValue, Tax, ProductAttribute, ProductCategory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                    'is_customer', 'is_superuser', 'is_staff',)

    exclude = ('password', 'last_login')

    list_filter = ('is_customer', 'is_superuser', 'is_staff',)
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ('user', 'credit_card', 'company',
                    'address_1', 'address_2',
                    'city', 'region', 'postal_code',
                    'country', 'shipping_region',
                    'day_phone', 'eve_phone',
                    'mob_phone',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discounted_price', 'image', 'image_2',
                    'description', 'thumbnail', 'display',)

    list_filter = ('name', 'price',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.get_fields()]

    list_filter = ('category', 'product',)


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'has_paid', 'customer', 'total_amount', 'created_on', 'shipped_on', 'status', 'comments',
                    'auth_code', 'reference', 'shipping', 'tax']

    list_filter = ('has_paid', 'created_on',)
    print(list_display)


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderDetail._meta.get_fields()]


@admin.register(ShippingRegion)
class ShippingRegionAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in ShippingRegion._meta.get_fields()]
    pass

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Shipping._meta.get_fields()]
    pass

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Tax._meta.get_fields()]
    pass

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'value']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductAttribute._meta.get_fields()]

