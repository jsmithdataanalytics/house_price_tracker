from property.zoopla import Zoopla
from utils.db import Database


def get_listings():
    Database().insert(table_name='Listings', rows=Zoopla().get_listings())
