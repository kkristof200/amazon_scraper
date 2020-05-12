from typing import List, Dict, Optional

from kov_utils.request import request

from .helpers.parser import Parser
from .utils.url_creator import AmazonURLCreator as URLCreator

class Amazon:
    def __init__(self):
        self.parser = Parser()

    def get_product_ids_and_next_page(self, url: str) -> (Optional[List[str]], Optional[str]):
        try:
            response = request(url)

            return (self.parser.parse_products_page(response), self.parser.next_products_page(response))
        except Exception as e:
            print('get_product_ids_and_next_page', e)

            return None, None

    def get_asins_from_grid_based_page(self, url: str) -> Optional[List[str]]:
        try:
            return self.parser.parse_products_page_grid_style(request(url))
        except Exception as e:
            print('get_asins_from_grid_based_page', e)

            return None

    def get_product_details(self, asin: str) -> Optional[Dict]:
        try:
            return self.parser.parse_product(
                request(URLCreator.create_product_url(asin))
            )
        except Exception as e:
            print('get_product_details', e)
            
            return None

    def get_product_reviews(self, asin: str) -> Optional[Dict]:
        try:
            return self.parser.parse_reviews(
                request(URLCreator.create_product_reviews_url(asin))
            )
        except Exception as e:
            print('get_product_reviews', e)

            return None