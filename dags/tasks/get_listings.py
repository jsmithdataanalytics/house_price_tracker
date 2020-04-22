from property.zoopla import Zoopla
from utils.db import InsertBuffer


def get_listings():
    InsertBuffer(size=500, table_name='Listings').run(Zoopla().get_listings())
