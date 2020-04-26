from property.zoopla import Zoopla
from utils import db


def get_listings():
    db.insert_or_replace(table_name='Listings', items=Zoopla().get_listings())
