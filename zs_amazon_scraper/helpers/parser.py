from typing import Optional, Dict, List
import json

from bs4 import BeautifulSoup

from kcu import strings

class Parser():
    def parse_product(self, response) -> Optional[Dict]:
        categories = []
        features = []
        video_urls = []

        soup = BeautifulSoup(response.content, 'lxml')
        try:
            parsed_json = json.loads(strings.between(response.text, 'var obj = jQuery.parseJSON(\'', '\')'))
        except Exception as e:
            print(e)
            
            return None

        title = parsed_json['title']
        asin = parsed_json['mediaAsin']
        images = parsed_json
        videos = parsed_json['videos']

        features = []

        try:
            for feature in soup.find('div', {'class':'a-section a-spacing-medium a-spacing-top-small'}).find_all('span', {'class':'a-list-item'}):
                try:
                    features.append(feature.get_text().strip())
                except:
                    pass
        except:
            pass

        try:
            categories_container = soup.find('div', {'id':'wayfinding-breadcrumbs_container'})

            for category_a in categories_container.find_all('a', {'class':'a-link-normal a-color-tertiary'}):
                try:
                    categories.append(BeautifulSoup(category_a.text, "lxml").text.replace('\\', '/').replace('<', ' ').replace('>', ' ').strip().lower())
                except:
                    pass
        except:
            pass

        # print('categories', categories)
        
        try:
            price_text = soup.find('span', {'id':'priceblock_ourprice'}).text.replace('$', '').strip()
            price = float(price_text)
        except:
            price = None

        table_for_product_info = soup.find('table', {'id':'productDetails_detailBullets_sections1', 'class':'a-keyvalue prodDetTable'})

        product_information_dict = {}
        if table_for_product_info is not None:
            for tr in table_for_product_info.find_all('tr'):
                key = tr.find('th').get_text().strip()

                if key is not None and key not in ['Customer Reviews', 'Best Sellers Rank']:
                    value = tr.find('td').get_text().strip()
                    product_information_dict[key] = value

        image_details = {}

        if 'colorToAsin' in images and images['colorToAsin'] is not None:
            colors = images['colorToAsin']

            for color_name, color_dict in colors.items():
                _asin = color_dict['asin']
                image_details[_asin] = {
                    'name' : color_name,
                    'image_urls' : []
                }
                
                images_by_color = images['colorImages'][color_name]

                for elem in images_by_color:
                    if 'hiRes' in elem: 
                        image_details[_asin]['image_urls'].append(elem['hiRes'])

            for url in videos:
                if 'url' in url:
                    video_urls.append(url['url'])
        
        if image_details is None or image_details == {}:
            try:
                images_json = json.loads(strings.between(response.text, '\'colorImages\': { \'initial\': ', '}]},') + '}]')

                image_details[asin] = {
                    'name' : asin,
                    'image_urls' : []
                }

                for image_json in images_json:
                    try:
                        image_details[asin]['image_urls'].append(image_json['large'])
                    except Exception as e:
                        print(e)
                        pass
            except:
                pass

        try:
            associated_asins_string = response.text.split('dimensionToAsinMap" : ')[1].split('},')[0]
            associated_asins_json = json.loads(associated_asins_string + '}')

            for val in associated_asins_json.values():
                associated_asins.append(val)
        except:
            associated_asins = []

        return {
            'title': title, 
            'price': price,
            'categories': categories,
            'features': features,
            'product information': product_information_dict,
            'images': image_details,
            'videos_url': video_urls,
            'associated_asins': associated_asins
        }
    
    def parse_reviews_with_images(self, response) -> Optional[List[Dict]]:
        # 'https://www.amazon.com/gp/customer-reviews/aj/private/reviewsGallery/get-data-for-reviews-image-gallery-for-asin?asin='
        try:
            reviews_json = json.loads(response.text)        
        except Exception as e:
            print(e)

            return None
        
        reviews = {} 
        details = reviews_json['images']

        for elem in details:
            try:
                author = elem['associatedReview']['author']['name']
                text = elem['associatedReview']['text']
                clean_text = BeautifulSoup(text, "lxml").text.replace('  ', ' ')
                review_key = author

                if review_key in reviews:
                    review = reviews[review_key]
                else:
                    review = {
                        'author':author,
                        'text': clean_text,
                        'rating':elem['associatedReview']['overallRating'],
                        'image_urls':[]
                    }

                    if 'scores' in elem['associatedReview'] and 'helpfulVotes' in elem['associatedReview']['scores']:
                        review['upvotes'] = int(elem['associatedReview']['scores']['helpfulVotes'])
                    else:
                        review['upvotes'] = 0
                
                img_url = elem['mediumImage']
                review['image_urls'].append(img_url)

                reviews[review_key] = review     
            except:
                pass

        return sorted(list(reviews.values()), key=lambda k: k['upvotes'], reverse=True)

    def parse_reviews(self, response) -> Optional[List[str]]:
        soup = BeautifulSoup(response.content, 'lxml')
        reviews = []

        for elem in soup.find_all('span', {'data-hook':'review-body'}):
            try:
                reviews.append({
                    'text':elem.find('span').get_text().strip(),
                    'rating':5
                })
            except:
                pass

        return reviews

    def parse_products_page_grid_style(self, response):
        soup = BeautifulSoup(response.content, 'lxml')
        asin_ids = []

        products_container = soup.find('ol', {'id':'zg-ordered-list'})
        
        for li in products_container.find_all('li'):
            try:
                product_url = li.find('a', href=True)
                asin = product_url['href'].split('dp/')[1].split('/')[0]
                asin_ids.append(asin)
            except Exception as e:
                print('parse_products_page_grid_style', e)

        return asin_ids

    def parse_products_page(self, response):   
        asin_ids = []
        soup = BeautifulSoup(response.content, 'lxml')
        results = soup.find_all('span', {'class':'a-declarative'})
        
        for elem in results:
            try:
                asin_id = strings.between(elem['data-a-popover'], 'asin=', '&')

                if asin_id is not None:
                    asin_ids.append(asin_id)
            except:
                pass
        
        return asin_ids

    def next_products_page(self, response):

        soup = BeautifulSoup(response.content, 'lxml')

        next_pag = soup.find('li', {'class':'a-last'})
        next_page_url = next_pag.find('a', href=True)

        return next_page_url['href']