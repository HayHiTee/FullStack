import random
import string
from datetime import datetime

from FullStackApp.models import Orders, Shipping

def generate_token(k=5):
    return ''.join(random.choices(string.digits, k=k))

# A class that creates a Cart Object from Model and
# generates unique token or tracking Id
# for each cart object stored in the model database
class CartOrder:
    def create_order(self, total_amount, shipping):
        trck_id = self._generate_tracking_id()
        while Orders.objects.filter(tracking_id=trck_id).exists():
            trck_id = self._generate_tracking_id()
        else:
            obj = Orders.objects.create(tracking_id=trck_id, total_amount=total_amount,
                                      tax_id=2, shipping=shipping)

            return obj

    def _generate_tracking_id(self):
        rand = generate_token(2)
        date_time = datetime.now()
        date = str(date_time.date()).replace('-', '')
        hr = str(date_time.hour)
        min = str(date_time.minute)
        sec = str(date_time.second)
        tracking_id = 'TRC/{}/{}{}/{}'.format(date, min, sec,  rand)
        return tracking_id