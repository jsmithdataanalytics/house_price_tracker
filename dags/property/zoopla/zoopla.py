import re
from datetime import datetime
from os import environ
from typing import Iterable, List, Dict

from bs4 import BeautifulSoup
from requests import Response

from property import PropertyLister
from utils.web import requests_retry_session


def format_zoopla_date(date_found) -> str:
    date_text = f'{date_found[1].rjust(2, "0")} {date_found[2]} {date_found[3]}' if date_found else None

    return str(datetime.strptime(date_text, '%d %b %Y').date()) if date_text else None


class Zoopla(PropertyLister):
    url = environ['ZOOPLA_SEARCH']
    outcode_regex = '(?:[^a-zA-Z0-9]|^)([A-Z]{1,2}\\d{1,2})(?:[^a-zA-Z0-9]|$)'
    listing_date_regex = '(\\d{1,2})(?:st|nd|rd|th)\\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+(\\d{4})'
    reduced_date_regex = 'Last\\s+reduced:\\s+' + listing_date_regex

    def __init__(self):
        pass

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
            listing_price = float(price_found[1].replace(',', '')) if price_found else None
            bedrooms_tag = listing.find(name='span', attrs={'class': 'num-beds'})
            num_bedrooms = int(bedrooms_tag.text.strip()) if bedrooms_tag else None
            outcodes = re.findall(Zoopla.outcode_regex, listing.find(attrs={'class': 'listing-results-address'}).text)
            outcode = outcodes[-1] if outcodes else None
            marketing_tag = listing.find(name='p', attrs={'class': 'listing-results-marketed'})
            marketing_text = marketing_tag.text if marketing_tag else None
            date_found = re.search(Zoopla.listing_date_regex, marketing_text) if marketing_text else None
            listed_on = format_zoopla_date(date_found)
            reduction_tag = listing.find(name='span', attrs={'class': 'listing_sort_copy'})
            reduction_text = reduction_tag.text if reduction_tag else None
            date_found = re.search(Zoopla.reduced_date_regex, reduction_text) if reduction_text else None
            last_reduced_on = format_zoopla_date(date_found)

            if price_found:
                page.append({
                    'listing_id': listing_id,
                    'listing_price': listing_price,
                    'num_bedrooms': num_bedrooms,
                    'outcode': outcode,
                    'listed_on': listed_on,
                    'last_reduced_on': last_reduced_on
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
