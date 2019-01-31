import unittest

from services_operations.es_service import EsService


host = "search-cars-3uxxqnojm2h2asargsvenswncq.us-east-1.es.amazonaws.com"


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.es = EsService(host)

    def test_search_lucene(self):

        search_pairs = {
            'order_id': 'o1'
        }

        response = self.es.search_lucene(search_pairs)
        print(response)
