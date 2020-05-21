from os import path

class AmazonURLCreator:
    @staticmethod
    def product_url(asin):
        return path.join('https://www.amazon.com', 'dp', asin)

    @staticmethod
    def product_reviews_with_images_url(asin):
        return 'https://www.amazon.com/gp/customer-reviews/aj/private/reviewsGallery/get-data-for-reviews-image-gallery-for-asin?asin=' + asin

    @staticmethod
    def product_reviews_url(asin, star_rating: str = 'five_star', page_num: int = 1):
        return 'https://www.amazon.com/product-reviews/' + asin + '/?ie=UTF8&reviewerType=all_reviews&filterByStar=' + star_rating + '&pageNumber=' + str(page_num)

    @staticmethod
    def next_page_url(next_page_param):
        next_page_url = 'https://www.amazon.com' + next_page_param
        return next_page_url