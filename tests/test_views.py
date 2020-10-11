"""
This is test module to ensure services
are behaving the way it is expected t behave

author: Pritesh
date: 11-10-2020 21:44
"""

import requests as client
import configparser
import json

headers = {'Content-type': 'application/json'}

config = configparser.ConfigParser()
config.read('config.ini')

base_url = config['client']['base_url']
product_name = config['search_product']['product_name']
product_category = config['search_product']['product_category']


def test_push_products_view():
    products = {"data" : [{ "product_id": "SHOEH4GRSUBJGZXE5", "product_name": "AW Bellies",
                            "merchant_name": "Flipkart", "listing_price": 1498.0, "sale_price": 999.0,
                            "discount": 499.0, "brand": "FW",
                            "description": "Key Features of AW Bellies Sandals Wedges Heel Casuals",
                            "rating": None, "reviews": "NA",
                            "url": "http://www.flipkart.com/aw-bellies/p/itmeh4grgfbkexnt?pid=SHOEH4GRSUBJGZXE",
                            "category_name": "Fashion"}]}

    response = client.post('{base_url}products/push/'.format(base_url=base_url),
                           data=json.dumps(products),
                           headers=headers
                        )
    assert 200 == response.status_code
    assert "1 record(s) inserted successfully" == response.json()["message"]


def test_push_products_batch_view():
    files = {'dataset': ('sample_dataset.xlsx',
                         open('sample_dataset.xlsx', 'rb'),
                         'application/vnd.ms-excel')}
    response = client.post('{base_url}products/push/batch/'.format(base_url=base_url),
                           files=files
                           )
    assert 200 == response.status_code
    assert "20 record(s) inserted successfully" == response.json()["message"]


def test_get_products_view():
    response = client.get('{base_url}products?product_name={product_name}'
                          '&product_category={product_category}'
                          .format(base_url=base_url,
                            product_name=product_name,
                            product_category=product_category)
                          )
    assert 200 == response.status_code
    assert "Records fetched successfully !" == response.json()["message"]