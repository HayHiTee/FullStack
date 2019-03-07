import json
import os
import sys

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR)
from FullStack.settings import BASE_DIR


class DataPopulation:
    file = ''

    def _read_json(self):
        path = 'init_data/json/{}'.format(self.file)
        path = os.path.join(BASE_DIR, path)
        data = ''
        with open(path) as f:
            data = json.load(f)
            print(data)
        return data

    def tax(self, file):
        self.file = file
        data = self._read_json()
        print(data)



if __name__ == '__main__':
    pop = DataPopulation()
    pop.tax('tax.json')

