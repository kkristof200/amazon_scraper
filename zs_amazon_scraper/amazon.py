from typing import List, Dict

import validators

from kov_utils.request import request

from .helpers.parser import Parser
from .utils.url_creator import AmazonURLCreator as URLCreator

class Amazon:
    def __init__(self):
        self.parser = Parser()

    def get_product_ids_and_next_page(self, url: str) -> (List[str], str):
        if validators.url(url):
            response = request(url)

            try:
                return (self.parser.parse_products_page(response), self.parser.next_products_page(response))
            except:
                pass

        return None, None

    def get_product_ids_from_grid_based_page(self, url: str) -> (List[str], str):
        if validators.url(url):
            response = request(url)

            try:
                asins = self.parser.parse_products_page_grid_style(response)
            except Exception as e:
                print('get_product_ids_from_grid_based_page', e)

                asins = None

        return asins, None

    def get_product(self, product_id: str) -> (Dict, List):        
        response_details = request(URLCreator.create_product_url(product_id))
        try:
            product_details = self.parser.parse_product(response_details)
        except Exception as e:
            print('parse_product', e)
            product_details = None

        response_reviews = request(URLCreator.create_product_reviews_url(product_id))
        try:
            product_reviews = self.parser.parse_reviews(response_reviews)
        except Exception as e:
            print('parse_reviews', e)
            product_reviews = None

        return product_details, product_reviews