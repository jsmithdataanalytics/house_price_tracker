from property.zoopla import Zoopla
from utils import db


def get_listings():
    db.insert(table_name='Listings', items=Zoopla().get_listings())
