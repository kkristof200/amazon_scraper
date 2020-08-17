from typing import List, Dict, Optional

from kcu.request import request

from .helpers.parser import Parser
from .utils.url_creator import AmazonURLCreator as URLCreator

class Amazon:
    def __init__(self):
        self.parser = Parser()

    def get_product_ids_and_next_page(
        self,
        url: str,
        user_agent: Optional[str] = None,
        random_ua: bool = True
    ) -> (Optional[List[str]], Optional[str]):
        try:
            response = request(url, user_agent=user_agent, fake_useragent=random_ua)

            return (self.parser.parse_products_page(response), self.parser.next_products_page(response))
        except Exception as e:
            print('get_product_ids_and_next_page', e)

            return None, None

    def get_asins_from_grid_based_page(
        self,
        url: str,
        user_agent: Optional[str] = None,
        random_ua: bool = True
    ) -> Optional[List[str]]:
        try:
            return self.parser.parse_products_page_grid_style(request(url, user_agent=user_agent, fake_useragent=random_ua))
        except Exception as e:
            print('get_asins_from_grid_based_page', e)

            return None

    def get_product_details(
        self,
        asin: str,
        user_agent: Optional[str] = None,
        random_ua: bool = True
    ) -> Optional[Dict]:
        try:
            return self.parser.parse_product(
                request(URLCreator.product_url(asin), user_agent=user_agent, fake_useragent=random_ua)
            )
        except Exception as e:
            print('get_product_details', e)
            
            return None

    def get_product_reviews_with_images(
        self,
        asin: str,
        user_agent: Optional[str] = None,
        random_ua: bool = True
    ) -> Optional[Dict]:
        try:
            return self.parser.parse_reviews_with_images(
                request(URLCreator.product_reviews_with_images_url(asin), user_agent=user_agent, fake_useragent=random_ua)
            )
        except Exception as e:
            print('get_product_reviews_with_images', e)

            return None

    def get_product_reviews(
        self,
        asin: str,
        star_rating: str = 'five_star',
        user_agent: Optional[str] = None,
        random_ua: bool = True
    ) -> Optional[List[Dict]]:
        try:
            return self.parser.parse_reviews(
                request(URLCreator.product_reviews_url(asin, star_rating=star_rating, page_num=1), user_agent=user_agent, fake_useragent=random_ua)
            )
        except Exception as e:
            print('get_product_reviews', e)

            return None