# compare_products

This Product Comparison service compares the similar products from different website and will provide the flexibility to check the available price from different merchants before deciding which one to buy.
This service is build on python Django REST framework.
# Table of Contents

   * [Service Product Comparison](#Service-Product-Comparison)
   * [How to run the Service](#how-to-run-the-Service)
      * [Installation](#installation)
         * [Clone the repository](#clone-the-repository)
         * [Install with virtualenv](#install-with-virtualenv)
      * [Run your python script](#run-your-python-script)
      * [Check the result](#check-the-result)
   * [Docker](#docker)
  

## How to run the Service

### Installation

#### Clone the repository

```bash
git clone git@github.com:pritesh543/compare_products.git
cd compare_products
```

#### Install with virtualenv
```bash
virtualenv --python=python[3.6|3.7|3.8] venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run your python script

To Run on default port (By default it runs on 8000)
```bash
python manage.py runserver
```
To run on specified port
```bash
python manage.py runserver [port]
```
## Check the result

- Endpoints to get the product details filtered by category and name:
```bash
http://127.0.0.1:[port]/products?product_name={product_name}&product_category={product_category}
```
Parameters: product_category, product_name.

- Endpoint to push the data into database:
```bash
http://127.0.0.1:[port]/products/push/
```
- Endpoint to batch import (upload file) into database:
currenly supported: `csv` , ``xlsx``
```bash
http://127.0.0.1:[port]/products/push/batch/
```