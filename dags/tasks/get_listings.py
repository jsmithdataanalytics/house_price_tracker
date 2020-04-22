from property.zoopla import Zoopla
from time import sleep


def get_listings():

    for listing in Zoopla().get_listings():
        print(listing)
        sleep(0.01)
