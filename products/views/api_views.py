# views here

# Django modules
from rest_framework import viewsets
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from products.models import Product
from ..serializers import ProductSerializer

class Constant:
    IS_ERROR = True
    FAILED_STATUS = "FAILED"
    DEFUALT_MSG = "Something Went Wrong"
    POST = "POST"
    GET = "GET"

class ProductView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super(ProductView, self).__init__(**kwargs)

    @action(
        detail = True,
        methods = [Constant.GET],
        # authentication_classes = [JWTAuthentication]
    )
    def get_products(self, request, *args, **kwargs):
        try:
            products = Product.objects.all()
            products_serializer = ProductSerializer(products, many=True)
            return JsonResponse(products_serializer.data, status=200, safe=False)
            #return Response(status=status.HTTP_200_OK, data=JsonResponse(products_serializer.data))
        except Exception as e:
            print("Exception: ", e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={})

    def push_products(self, request, *args, **kwargs):
        try:
            pass
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={})
