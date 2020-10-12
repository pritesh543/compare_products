# API Documentation
This API uses `POST` & ``GET`` request to communicate and HTTP [response codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to identify status and errors. All responses come in standard JSON. 
### Response Codes
```
200: Success
400: Bad request
404: Cannot be found
405: Method not allowed
50X: Server Error
```

### Example Error Message
```json
http code 400

{
    "status": 206,
    "message": "key missing in request",
    "is_error": true
}
```

## (1) Compare Products
**You send:**  product_name & product_category.
**You get:** List of products with competitive prices from different merchants.

**Request:**
```json
GET /products?product_name={product_name}&product_category={product_category} HTTP/1.1
Accept: application/json
Content-Type: application/x-www-form-urlencoded

{
    "product_name": "Womens shorts",
    "product_category": "Fashion" 
}
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Server: WSGIServer/0.2 CPython/3.8.6
Content-Type: application/json
Content-Length: 2518

{
    "message": "Records fetched successfully !",
    "is_error": false,
    "status": 200,
    "product_details": [
        {
            "id": 228,
            "product_id": "SRTEH2F6HUZMQ6SJ4",
            "product_name": "Alisha Solid Women's Cycling Shorts",
            "merchant_name": "Myntra",
            "listing_price": 966.0,
            "sale_price": 699.0,
            "discount": 267.0,
            "brand": "Alisha",
            "description": "Key Features of Alisha Solid Women's Short",
            "rating": null,
            "reviews": "NA",
            "url": "http://www.flipkart.com/alisha-solid-women-s-cycling-shorts/p/itmeh2f6sdgah2pq?pid=SRTEH2F6HUZMQ6SJ",
            "category_name": "Fashion"
        }
    ]
}
```

## (2) Push Products
**You send:**  json data.
**You get:** count of records inserted.

**Request:**
```json
POST /products/push/ HTTP/1.1
Accept: application/json
Content-Type: application/json

{
    "data"  :  [
                    {
                        "product_id": "SHOEH4GRSUBJGZXE4",
                        "product_name": "AW Bellies",
                        "merchant_name": "Flipkart",
                        "listing_price": 1498.0,
                        "sale_price": 999.0,
                        "discount": 499.0,
                        "brand": "FW",
                        "description": "Key Features of AW Bellies Sandals Wedges Heel Casuals,AW Bellies Price: Rs. 499 Material: Synthetic Lifestyle: Casual Heel Type: Wedge Warranty Type: Manufacturer Product Warranty against manufacturing defects: 30 days Care....",
                        "rating": null,
                        "reviews": "NA",
                        "url": "http://www.flipkart.com/aw-bellies/p/itmeh4grgfbkexnt?pid=SHOEH4GRSUBJGZXE",
                        "category_name": "Fashion"
                    }
                ]
}
```

**Successful Response:**
```json
HTTP/1.1 200 OK
Server: WSGIServer/0.2 CPython/3.8.6
Content-Type: application/json
Content-Length: 82

{
    "message": "1 record(s) inserted successfully",
    "is_error": false,
    "status": 200
}

```

**Failed Response:**
```json
HTTP/1.1 500 Internal-Server-Error
Server: WSGIServer/0.2 CPython/3.8.6
Content-Type: application/json
Content-Length: 82

{
    "code": 500,
    "message": "exception {e}",
    "is_error": true
}
``` 

## (3) Push Products (batch import - upload file)
**You send:**  file with requisite format.
**You get:** count of records inserted.

**Request:**
```json
POST /products/push/batch/ HTTP/1.1
Accept: application/vnd.ms-excel
Content-Type: multipart/form-data

files = {'dataset': ('sample_dataset.xlsx',
                         open('sample_dataset.xlsx', 'rb'),
                         'application/vnd.ms-excel')}

```
* [Sample Dataset (file to upload)](/compare_products/products/tests/sample_dataset.xlsx)


**Successful Response:**
```json
HTTP/1.1 200 OK
Server: WSGIServer/0.2 CPython/3.8.6
Content-Type: application/json
Content-Length: 82

{
    "message": "1 record(s) inserted successfully",
    "is_error": false,
    "status": 200
}

```

**Failed Response:**
```json
HTTP/1.1 500 Internal-Server-Error
Server: WSGIServer/0.2 CPython/3.8.6
Content-Type: application/json
Content-Length: 82

{
    "code": 500,
    "message": "exception {e}",
    "is_error": true
}
``` 

## (4) Pull Products (from merchant/data source)
**You send:**  merchant_code
**You get:** count of records inserted.

**Request:**
```json
POST /products/pull/{merchant_code} HTTP/1.1
Accept: */*
Content-Type: application/text

TryOut: AMAZON 'OR' WALMART 'OR' ADIDAS
POST /products/pull/AMAZON HTTP/1.1
POST /products/pull/WALMART HTTP/1.1
POST /products/pull/ADIDAS HTTP/1.1

```
* [Sample Datasource To Pull - ADIDAS](/compare_products/products/pull_dataset/adidas_sample_dataset.json)
* [Sample Datasource To Pull - AMAZON](/compare_products/products/pull_dataset/amazon_sample_dataset.json)
* [Sample Datasource To Pull - WALMART](/compare_products/products/pull_dataset/walmart_sample_dataset.json)

**Successful Response:**
```json
HTTP/1.1 200 OK
Server: WSGIServer/0.2 CPython/3.8.6
Content-Type: application/json
Content-Length: 82

{
    "message": "20 record(s) inserted successfully",
    "is_error": false,
    "status": 200
}

```

**Failed Response:**
```json
HTTP/1.1 200 OK
Server: WSGIServer/0.2 CPython/3.8.6
Content-Type: application/json
Content-Length: 82

{
    "code": 200,
    "message": "No Data Available or merchant_code not found !",
    "is_error": true
}
```