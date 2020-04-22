import re
from typing import Iterable, List, Dict

from airflow.hooks.http_hook import HttpHook
from bs4 import BeautifulSoup
from requests import Response

from property import PropertyLister
from utils.web import requests_retry_session


class Zoopla(PropertyLister):
    conn_id = 'zoopla'
    outcode_regex = '(?:[^a-zA-Z0-9]|^)([A-Z]{1,2}\\d{1,2})(?:[^a-zA-Z0-9]|$)'

    def __init__(self):
        self.url = HttpHook.get_connection(Zoopla.conn_id).host

    def __get_page(self, page_number: int) -> List[Dict]:
        page = []
        response = self.__make_request(page_number=page_number)
        soup = BeautifulSoup(response.text, 'html.parser')
        ul = soup.find(name='ul', attrs={'class': 'listing-results'})
        listings = ul.find_all(name='li', attrs={'data-listing-id': True})

        for listing in listings:
            listing_id = listing.attrs['data-listing-id']
            price_text = listing.find(name='a', attrs={'class': 'listing-results-price'}).text
            price_found = re.search('£([0-9.,]+)', price_text)
            bedrooms_tag = listing.find(name='span', attrs={'class': 'num-beds'})
            num_bedrooms = int(bedrooms_tag.text.strip()) if bedrooms_tag else None
            outcodes = re.findall(Zoopla.outcode_regex, listing.find(attrs={'class': 'listing-results-address'}).text)
            outcode = outcodes[-1] if outcodes else None

            if price_found:
                listing_price = float(price_found[1].replace(',', ''))
                page.append({
                    'listing_id': listing_id,
                    'listing_price': listing_price,
                    'num_bedrooms': num_bedrooms,
                    'outcode': outcode
                })

        return page

    def __make_request(self, page_number: int) -> Response:
        print(f'Requesting Zoopla listings (page {page_number})...')
        response = requests_retry_session().get(self.url, params={'pn': page_number}, timeout=5)
        print('Success.')

        return response

    def get_listings(self) -> Iterable:
        page_number = 0

        while True:
            page_number += 1
            listings_page = self.__get_page(page_number=page_number)

            if not listings_page:
                break

            while listings_page:
                yield listings_page.pop()
