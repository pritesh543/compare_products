from django.conf.urls import url

from products.views import api_views as api

urlpatterns = [
    url(r'^products/{id}/', api.ProductView.as_view({'get':'get_products'}),
        name='get_product'),

    url(r'products/', api.ProductView.as_view({'get':'get_products'}),
        name='get_products'),

    url(r'products/{product_name}/{product_category}/',
        api.ProductView.as_view({'get':'get_products'}),
        name='get_products_search')
]