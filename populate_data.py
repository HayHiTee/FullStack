import json
import os
import sys
import FullStack

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FullStack.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'FullStack.settings'
import django

django.setup()
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR)
from FullStack.settings import BASE_DIR
from FullStackApp.models import Tax, Attribute, AttributeValue, Category, Department, Product, ProductAttribute, \
    ProductCategory, Shipping, ShippingRegion


class DataPopulation:
    file = None

    def _read_json(self):
        if self.file is not None:
            path = 'init_data/json/{}'.format(self.file)
            path = os.path.join(BASE_DIR, path)
            data = ''
            with open(path) as f:
                data = json.load(f)
                print(data)
            return data
        print('invalid filename')
        return []

    def _add_data(self, my_model):
        data = self._read_json()
        print(data)
        mod = my_model.objects.bulk_create(
            [my_model(**q) for q in data if not my_model.objects.filter(id=q['id']).exists()])
        print(mod)

    def tax(self, file):
        self.file = file
        self._add_data(Tax)

    def attribute(self, file):
        self.file = file
        self._add_data(Attribute)

    def attribute_value(self, file):
        self.file = file
        self._add_data(AttributeValue)

    def category(self, file):
        self.file = file
        self._add_data(Category)

    def department(self, file):
        self.file = file
        self._add_data(Department)

    def product(self, file):
        self.file = file
        self._add_data(Product)

    def product_attribute(self, file):
        self.file = file
        data = self._read_json()
        print(data)
        product = ProductAttribute.objects.bulk_create(
            [ProductAttribute(**q) for q in data if
             not ProductAttribute.objects.filter(product=q['product_id'], attribute_value=q['attribute_value_id']).exists()])
        print(product)

    def product_category(self, file):
        self.file = file
        data = self._read_json()
        print(data)
        product_category = ProductCategory.objects.bulk_create(
            [ProductCategory(**q) for q in data if
             not ProductCategory.objects.filter(product=q['product_id']).exists()])
        print(product_category)

    def shipping(self, file):
        self.file = file
        self._add_data(Shipping)

    def shipping_region(self, file):
        self.file = file
        self._add_data(ShippingRegion)

    def execute_data(self):
        self.tax('tax.json')
        self.department('department.json')
        self.category('category.json')
        self.product('product.json')
        self.product_category('product_category.json')
        self.attribute('attribute.json')
        self.attribute_value('attribute_value.json')
        self.product_attribute('product_attribute.json')
        self.shipping_region('shipping_region.json')
        self.shipping('shipping.json')


if __name__ == '__main__':
    pop = DataPopulation()
    pop.execute_data()
