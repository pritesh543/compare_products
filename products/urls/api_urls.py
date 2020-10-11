from django.conf.urls import url

from products.views import api_views as api

urlpatterns = [

    url(r'^products/$',
        api.ProductView.as_view({'get':'get_products'}),
        name='get_products'),

    url(r'^products/push/$',
        api.ProductView.as_view({'post':'create_products'}),
        name='create_products'),

    url(r'^products/push/batch/$',
        api.ProductView.as_view({'post':'create_products_batch'}),
        name='create_products')

]