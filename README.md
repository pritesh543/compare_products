# compare_products

This "Product Comparison" service compares the similar products from different website(s) and retail stores and provides the flexibility to check the available price from different merchants before deciding which one to buy.
This service is build on python Django REST framework.
# Table of Contents

   * [Service Product Comparison](#Service-Product-Comparison)
   * [How to run the Service](#how-to-run-the-Service)
      * [Installation](#installation)
         * [Clone the repository](#clone-the-repository)
         * [Run on Docker](#run-on-docker)
         * [To Run Manually](#to-run-manually)
      * [API Documentation](#api-documentation)


## How to run the Service

### Installation

#### Clone the repository

```bash
git clone git@github.com:pritesh543/compare_products.git
cd compare_products
```

## Run on Docker

Create and Push the image 

```bash
docker build -t comp-product-app -f Dockerfile .
```
Run the Image
```bash
docker run -it -p 8000:8000 comp-product-app
```

## To Run Manually

#### Install with virtualenv
```bash
virtualenv --python=python[3.6|3.7|3.8] venv
source venv/bin/activate
pip install -r requirement.txt
```

#### Run service
To Run on default port (By default it runs on 8000)
```bash
python manage.py runserver
```
To run on specified port
```bash
python manage.py runserver [port]
```
## API Documentation

Please refer API Documentation Available on repository.
* [API Docs](https://github.com/pritesh543/compare_products/blob/master/APIDocument.md)
