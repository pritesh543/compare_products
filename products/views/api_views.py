# views here

# Django modules
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import status

from products.serializers import ProductSerializer
from products.bll.product_bll import ProductManager

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
        """
        :param request: request
        :param args:
        :param kwargs: product_name, product_category
        :return: api_resp
        """
        api_resp = {
            "message": "Some Error !",
            "is_error": True,
            "status": status.HTTP_400_BAD_REQUEST,
        }
        message = ""

        if "product_name" not in request.query_params:
            message += "q_param: key missing `product_name`"

        if "product_category" not in request.query_params:
            message += "q_param: key missing `product_category`"

        if message:
            api_resp["message"] = message
            return JsonResponse(api_resp, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)

        q_product_name = request.query_params.get('product_name')
        q_product_category = request.query_params.get('product_category')

        products = ProductManager().get_relevant_products(q_product_category, q_product_name)
        products_serializer = ProductSerializer(products, many=True)

        api_resp["status"] = status.HTTP_200_OK
        api_resp["message"] = "Records fetched successfully !"
        api_resp["is_error"] = False
        api_resp["product_details"] = sorted(products_serializer.data,
                                             key=lambda k: (k['rating'] is not None,
                                                            k['rating']), reverse=True)

        return JsonResponse(api_resp, status=status.HTTP_200_OK, safe=False)


    @action(
        detail=True,
        methods=[Constant.POST],
        # authentication_classes=[JWTAuthentication]
    )
    def create_products(self, request, *args, **kwargs):
        """

        :param request: request
        :param args:
        :param kwargs: file or json
        :return: api_resp
        """
        api_resp = {
            "message": "Some Error !",
            "is_error": True,
            "status": status.HTTP_400_BAD_REQUEST,
        }

        request_data = request.data.get("data", None)
        # request_data = json.loads(request.body).get("data", None)

        if request_data is None:
            api_resp["message"] = "`data` key is missing in request"
            return JsonResponse(api_resp, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)

        result_message = ProductManager().create_product(request_data)

        api_resp["status"] = status.HTTP_200_OK
        api_resp["message"] = result_message
        api_resp["is_error"] = False

        return JsonResponse(api_resp, status=status.HTTP_200_OK, safe=False)


    @action(
        detail=True,
        methods=[Constant.POST],
        # authentication_classes=[JWTAuthentication]
    )
    def create_products_batch(self, request, *args, **kwargs):
        """

        :param request: request
        :param args:
        :param kwargs: file or json
        :return: api_resp
        """
        api_resp = {
            "message": "Some Error !",
            "is_error": True,
            "status": status.HTTP_400_BAD_REQUEST,
        }

        if request.FILES:
            file_name = request.FILES['dataset'].name
            err_flag, err_message = ProductManager().check_file_extension(file_name)
            if not err_flag:
                api_resp["message"] = err_message
                return JsonResponse(api_resp, status=status.HTTP_502_BAD_GATEWAY, safe=False)

            try:
                if file_name.endswith(".csv"):
                    df_file = pd.read_csv(request.FILES['dataset'])
                elif file_name.endswith(".xlsx"):
                    df_file = pd.read_excel(request.FILES['dataset'])

                request_data = df_file.to_dict('records')
                result_message = ProductManager().create_product(request_data)

                api_resp["status"] = status.HTTP_200_OK
                api_resp["message"] = result_message
                api_resp["is_error"] = False

                return JsonResponse(api_resp, status=status.HTTP_200_OK, safe=False)

            except Exception as e:
                api_resp["message"] = str(e)
                return JsonResponse(api_resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        else:
            api_resp["message"] = "File Missing, please upload file !"
            return JsonResponse(api_resp, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)