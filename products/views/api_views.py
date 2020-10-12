"""
This is main file which is
directly called by our api's endpoints
this is kind of controller
which interacts with BLL & Integrators

last-edit: 12-10-2020 17:04
version: v1.0
"""

# Django modules
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import status

from common.logger import CustomLogger

from products.serializers import ProductSerializer
from products.bll.product_bll import ProductManager
from products.bll.product_integrators import ProductIntegrator

import pandas as pd

logger = CustomLogger.get_logger(__name__)
logger.info("initiating api-views")

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
        compare products service
        which searches product's basis
        filter provided

        :param request: request
        :param args:
        :param kwargs: product_name, product_category
        :return: Products (list of objects)
        """

        # sample response format
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
            logger.debug(message)
            return JsonResponse(api_resp, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)

        # reading query params
        q_product_name = request.query_params.get('product_name')
        q_product_category = request.query_params.get('product_category')
        logger.info(request.query_params)

        # calling bll for list of matching products
        logger.info("calling business logic....")
        products = ProductManager().get_relevant_products(q_product_category, q_product_name)
        products_serializer = ProductSerializer(products, many=True)

        # final response preparation
        logger.info("preparing final api response..")
        api_resp["status"] = status.HTTP_200_OK
        api_resp["message"] = "Records fetched successfully !"
        api_resp["is_error"] = False
        api_resp["product_details"] = sorted(products_serializer.data,
                                             key=lambda k: (k['rating'] is not None,
                                                            k['rating']), reverse=True)
        logger.info("product_details are sorted basis ratings.")
        logger.info("fetched " + str(len(api_resp["product_details"])) + " records.")

        return JsonResponse(api_resp, status=status.HTTP_200_OK, safe=False)

    @action(
        detail=True,
        methods=[Constant.POST],
        # authentication_classes=[JWTAuthentication]
    )
    def create_products(self, request, *args, **kwargs):
        """
        This service creates the
        objects in database
        on request data

        :param request: request
        :param args:
        :param kwargs: file or json
        :return: response message(success/error)
        """
        # final response format
        api_resp = {
            "message": "Some Error !",
            "is_error": True,
            "status": status.HTTP_400_BAD_REQUEST,
        }

        logger.info("create products service....")
        # parsing the request body
        # request_data = json.loads(request.body).get("data", None)
        request_data = request.data.get("data", None)

        if request_data is None:
            api_resp["message"] = "`data` key is missing in request"
            logger.debug("`data` key is missing in request")
            return JsonResponse(api_resp, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)

        # calling bll to create objects
        result_message = ProductManager().create_product(request_data)
        logger.info(result_message)

        # response preparation
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
        This services creates the objects in database
        while reading from file ie. via batch import service

        :param request: request
        :param args:
        :param kwargs: file or json
        :return: api_resp
        """
        # final response format
        api_resp = {
            "message": "Some Error !",
            "is_error": True,
            "status": status.HTTP_400_BAD_REQUEST,
        }

        logger.info("create products batch import service ...")

        # checking if file(s) is present in request
        if request.FILES:
            file_name = request.FILES['dataset'].name
            err_flag, err_message = ProductManager().check_file_extension(file_name)
            if not err_flag:
                api_resp["message"] = err_message
                logger.debug(err_message)
                return JsonResponse(api_resp, status=status.HTTP_502_BAD_GATEWAY, safe=False)

            # try block if file is not good
            try:
                if file_name.endswith(".csv"):
                    df_file = pd.read_csv(request.FILES['dataset'])
                elif file_name.endswith(".xlsx"):
                    df_file = pd.read_excel(request.FILES['dataset'])
                else:
                    df_file = None

                request_data = df_file.to_dict('records')
                result_message = ProductManager().create_product(request_data)

                # success response from here
                api_resp["status"] = status.HTTP_200_OK
                api_resp["message"] = result_message
                api_resp["is_error"] = False

                return JsonResponse(api_resp, status=status.HTTP_200_OK, safe=False)

            except Exception as e:
                logger.exception(e)
                api_resp["message"] = str(e)
                return JsonResponse(api_resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
        else:
            api_resp["message"] = "File Missing, please upload file !"
            logger.debug("File Missing, please upload file !")
            return JsonResponse(api_resp, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)

    @action(
        detail=True,
        methods=[Constant.POST],
        # authentication_classes=[JWTAuthentication]
    )
    def pull_products(self, request, *args, **kwargs):
        """
        Pull(s) product data from different
        data sources to create objects in database
        --> right now from pull_dataset dir
            basis merchant_code/merchant_name

        :param request: request
        :param args: merchant_code
        :param kwargs:
        :return: message (success/failure)
        """
        # final response format
        api_resp = {
            "message": "Some Error !",
            "is_error": True,
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

        logger.info("pull products service....")

        # calling bll to pull records & create objects in db
        merchant_code = kwargs.get("merchant_code")
        pull_response, response_message = ProductIntegrator(merchant_code).pull_records()

        if pull_response is False:
            logger.debug(response_message)
            api_resp["message"] = response_message
            return JsonResponse(api_resp, status=status.HTTP_206_PARTIAL_CONTENT, safe=False)

        # final response preparation
        api_resp["status"] = status.HTTP_200_OK
        api_resp["message"] = response_message
        api_resp["is_error"] = False

        logger.info(response_message)

        return JsonResponse(api_resp, status=status.HTTP_200_OK, safe=False)
