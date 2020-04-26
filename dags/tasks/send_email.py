import pandas as pd
from utils import db


def send_email():
    listings = pd.DataFrame(db.select_all('Listings'))
    listings.drop('id', axis=1, inplace=True)
    listings.set_index('listing_id', inplace=True)
    listings = listings.astype({'num_bedrooms': 'float64', 'listed_on': 'datetime64', 'last_reduced_on': 'datetime64'})

    return listings
