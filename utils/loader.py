#!/usr/bin/env python3
"""
Demo script that:
- reduces the price of everything in the camera category by 20% and then round to the lowest full number;
- sends the data to algolia.
"""

__author__ = "Enrico Vianello"

import argparse
import json
import os
from algoliasearch.search_client import SearchClient


APP_ID = os.environ['ALGOLIA_APP_ID']
API_KEY = os.environ['ALGOLIA_ADMIN_KEY']
INDEX_NAME = os.environ['ALGOLIA_INDEX']

PRICE_CHANGE_VALUE = .8  # relative price change for the items in the PRICE_CHANGE_CATEGORY category
PRICE_CHANGE_CATEGORY = "Cameras & Camcorders"


def main(args):
    """ Main entry point of the app """
    
    with open(args.input_file, "r") as f:
        products = json.load(f)

    # update products
    updated = 0
    updated_products = []
    for product in products:
        if product["categories"] and PRICE_CHANGE_CATEGORY in product["categories"]:
            product["price"] *= PRICE_CHANGE_VALUE
            product["price"] = int(product["price"]) # round to the floor integer
            updated += 1
        updated_products.append(product)

    # upload updated products    
    client = SearchClient.create(APP_ID, API_KEY)
    index = client.init_index(INDEX_NAME)

    index.save_objects(updated_products)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="Path of the json file containing the catalog data")
    args = parser.parse_args()

    main(args)