from bs4 import BeautifulSoup
import requests

from .models import ScrapingConfigDetail, ImageResult
from .forms import ScrapingForm


class scraping():

    def __init__(self, data):
        self.data = data
        self.scraping_config_id = self.data.get('scraping_config_id')
        self.product_name = str()
        self.product_price = str()
        self.headers = {
            'dnt': '1',
            'upgrade-insecure-requests': '10',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            # 'referer': 'https://www.amazon.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, i):
        if type(i) is not dict : raise Exception("must be dict data")
        if not i: raise Exception("data cannot be empty")
        self._data = i
    
    @property
    def scraping_config_id(self):
        return self._scraping_config_id
    
    @scraping_config_id.setter
    def scraping_config_id(self, i):
        if not i : raise Exception("scraping_config_id cannot be empty")
        self._scraping_config_id = i

    
    def _process(self):
        r = requests.get(self.data.get('link'), headers=self.headers)
        soup = BeautifulSoup(r.content)

        # Get attrs from detail config
        detail_attrs = ScrapingConfigDetail.objects.filter(scraping_config_id=self.scraping_config_id)
        
        for da in detail_attrs:
            if da.get_result == 'name':
                self.product_name = soup.find(da.taging, attrs={da.attribute_key: da.attribute_value})
            elif da.get_result == 'price':
                self.product_price = soup.find(da.taging, attrs={da.attribute_key: da.attribute_value})
            elif da.get_result == 'image_url':
                list_image = soup.findAll(da.taging, attrs={da.attribute_key: da.attribute_value})

                for l in list_image:
                    if 'amazon.com' in da.scraping_config.base_url:
                        image_uri = l.find('img') if l.find('img') else ''
                        image_uri = image_uri.attrs['src'].replace('40_.jpg', '500_.jpg') if image_uri else None
                    elif 'ebay.com' in da.scraping_config.base_url:
                        image_uri = l.attrs['src'].replace('64.jpg', '500.jpg') if l.attrs['src'] else ""
                    # TODO any ecommerce
                    else:
                        image_uri = None
                    
                    if image_uri:
                        image_result = {
                            'image_url' : image_uri,
                            'scraping_result_id':self.data.get('id')
                            } 
                        ImageResult.objects.create(**image_result)

        self.product_name = self.product_name.text if self.product_name else ''
        self.product_price = self.product_price.text if self.product_price else ''
        self.data['name'] = self.product_name
        self.data['price'] = self.product_price
        
        ScrapingForm().update(self.data)



def ready_scraping(data):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '10',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        # 'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    r = requests.get(data.get('link'), headers=headers)
    soup = BeautifulSoup(r.content)

    # Get attrs from detail config
    detail_attrs = ScrapingConfigDetail.objects.filter(scraping_config_id=data.get('scraping_config_id'))
    
    product_name = str()
    product_price = str()
    for da in detail_attrs:
        if da.get_result == 'name':
            product_name = soup.find(da.taging, attrs={da.attribute_key: da.attribute_value})
        elif da.get_result == 'price':
            product_price = soup.find(da.taging, attrs={da.attribute_key: da.attribute_value})
        elif da.get_result == 'image_url':
            list_image = soup.findAll(da.taging, attrs={da.attribute_key: da.attribute_value})

            for l in list_image:
                if 'amazon.com' in da.scraping_config.base_url:
                    image_uri = l.find('img') if l.find('img') else ''
                    image_uri = image_uri.attrs['src'].replace('40_.jpg', '500_.jpg') if image_uri else None
                elif 'ebay.com' in da.scraping_config.base_url:
                    image_uri = l.attrs['src'].replace('64.jpg', '500.jpg') if l.attrs['src'] else ""
                # TODO any ecommerce
                else:
                    image_uri = None
                
                if image_uri:
                    image_result = {
                        'image_url' : image_uri,
                        'scraping_result_id':data.get('id')
                        } 
                    ImageResult.objects.create(**image_result)

    product_name = product_name.text if product_name else ''
    product_price = product_price.text if product_price else ''
    data['name'] = product_name
    data['price'] = product_price
    
    ScrapingForm().update(data)