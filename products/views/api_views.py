# views here

# Django modules
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from products.models import Product
from ..serializers import ProductSerializer
from ..bll.product_bll import ProductManager

import json
import pandas as pd

class Constant:
    IS_ERROR = True
    FAILED_STATUS = "FAILED"
    DEFAULT_MSG = "Something Went Wrong"
    POST = "POST"
    GET = "GET"

class ProductView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super(ProductView, self).__init__(**kwargs)

    @action(
        detail=True,
        methods=[Constant.GET],
        # authentication_classes=[JWTAuthentication]
    )
    def get_products(self, request, *args, **kwargs):
        try:
            if "product_name" not in request.query_params:
                return Response(status=status.HTTP_206_PARTIAL_CONTENT, data={})

            if "product_category" not in request.query_params:
                return Response(status=status.HTTP_206_PARTIAL_CONTENT, data={})

            q_product_name = request.query_params.get('product_name')
            q_product_category = request.query_params.get('product_category')

            products = ProductManager().get_relevant_products(q_product_category, q_product_name)
            products_serializer = ProductSerializer(products, many=True)
            return JsonResponse(products_serializer.data, status=status.HTTP_200_OK, safe=False)

        except Exception as e:
            print("Exception: ", e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={})

    @action(
        detail=True,
        methods=[Constant.POST],
        # authentication_classes=[JWTAuthentication]
    )
    def create_products(self, request, *args, **kwargs):
        try:
            if request.FILES:
                file_name = request.FILES['dataset'].name
                print("file_name: ", file_name)

                if file_name.endswith(".csv"):
                    df_file = pd.read_csv(request.FILES['dataset'])
                elif file_name.endswith(".xlsx"):
                    df_file = pd.read_excel(request.FILES['dataset'])
                else:
                    return {"message" : "only csv or xlsx supported as of now."}

                request_data = df_file.to_dict('records')
                result_message = ProductManager().create_product(request_data)
                return JsonResponse({"message": result_message}, status=status.HTTP_200_OK, safe=False)
            else:
                request_data = json.loads(request.body).get("data", None)
                if request_data is None:
                    return JsonResponse({"message" : ""}, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)

                result_message = ProductManager().create_product(request_data)
                return JsonResponse({"message": result_message}, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            print("Error: ", e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={})
