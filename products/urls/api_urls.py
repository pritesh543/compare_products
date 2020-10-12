"""
This is product service API & endpoints
declaration module
i.e basically a API blueprint
"""

from django.conf.urls import url
from products.views import api_views as api

urlpatterns = [

    # url for comparing products takes two query params
    # i.e product_name & product_category
    url(r'^products/$',
        api.ProductView.as_view({'get': 'get_products'}),
        name='get_products'),

    # url for pushing the products in json format
    url(r'^products/push/$',
        api.ProductView.as_view({'post': 'create_products'}),
        name='create_products'),

    # url for batch import - csv/xlsx file supported
    # i.e upload file here
    url(r'^products/push/batch/$',
        api.ProductView.as_view({'post': 'create_products_batch'}),
        name='create_products'),

    # url for pulling the data from merchant data source
    # takes one parameter merchant_code
    url(r'products/pull/(?P<merchant_code>[\w\-]+)/$',
        api.ProductView.as_view({'get': 'pull_products'}),
        name='pull_products'),

    # url for ai_rating basis product_name & brand
    # takes two params product_name & brand
    url(r'products/ai_rating/<product_name>/<brand>$',
        api.ProductView.as_view({'get': 'pull_products'}),
        name='ai_rating'),
]
