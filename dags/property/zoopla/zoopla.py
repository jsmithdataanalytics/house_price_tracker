from property import PropertyLister
from typing import Iterable, List, Dict
from utils.web import requests_retry_session
from requests import Response
from time import sleep
from airflow.hooks.http_hook import HttpHook


class Zoopla(PropertyLister):
    page_size = 100
    rate_limit_header = ('X-Mashery-Error-Code', 'ERR_403_DEVELOPER_OVER_RATE')
    output_types = {'county', 'country', 'town', 'outcode', 'postcode'}
    api_key_cycle_sleep = 600
    conn_id = 'zoopla'

    def __init__(self):
        self.url = None
        self.api_keys = None
        self.current_api_key_number = None

    def __fetch_connections(self):
        connection = HttpHook.get_connection(Zoopla.conn_id)

        self.url = f'https://{connection.host}/{connection.schema}'
        self.api_keys = connection.extra_dejson['api_keys']
        self.current_api_key_number = 0

    def __get_current_api_key(self):
        return self.api_keys[self.current_api_key_number]

    def __rotate_api_key(self):
        self.current_api_key_number = (self.current_api_key_number + 1) % len(self.api_keys)

    def __get_page(self, query: str, by: str, page_number: int) -> List[Dict]:

        while True:
            response = self.__make_request(
                query=query,
                by=by,
                page_number=page_number,
                api_key=self.__get_current_api_key()
            )

            if response.status_code == 200:
                return response.json().get('listing') or []

            if response.status_code == 403 and Zoopla.rate_limit_header in response.headers.items():
                # if you get this 403, your api key has been rate limited (max 100 calls/hour)
                self.__rotate_api_key()

                if self.current_api_key_number == 0:
                    # if you have been through all api keys, wait 10 minutes to avoid excess calls
                    sleep(Zoopla.api_key_cycle_sleep)

            else:
                response.raise_for_status()
                raise Exception(f'Unexpected HTTP status code: {response.status_code}')

    def __make_request(self, query: str, by: str, page_number: int, api_key: str) -> Response:
        assert by in Zoopla.output_types

        params = {
            by: query,
            'output_type': by,
            'property_type': 'houses',
            'listing_status': 'sale',
            'page_number': page_number,
            'page_size': Zoopla.page_size,
            'api_key': api_key
        }

        return requests_retry_session().get(self.url, params=params, timeout=5)

    def get_listings(self, query: str, by: str) -> Iterable:
        self.__fetch_connections()
        page_number = 0

        while True:
            page_number += 1
            listings_page = self.__get_page(query=query, by=by, page_number=page_number)

            if not listings_page:
                break

            while listings_page:
                yield listings_page.pop()
