"""
This is a integration layer
where you can plug in multi-data source
by consuming their api's
"""

import os
import json
from compare_products.settings import BASE_DIR
from products.bll.product_bll import ProductManager
from common.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)
logger.info("product-integrator....")

# setting data dir path
module_dir = os.path.join(BASE_DIR, 'products')
data_dir = os.path.join(module_dir, 'pull_dataset')

logger.info("data_dir: " + data_dir)

class ProductIntegrator:
    """
    Simple product integrator
    to pull data from different
    data sources
    """
    def __init__(self, merchant_code):
        """
        initializing merchant code
        on default constructor

        :param merchant_code:
        """
        self.merchant_code = merchant_code

    def get_auth_token(self):
        """
        get api credentials from here
        basis merchant_code
        """
        # api_key = auth(self.merchant_code)
        pass

    def pull_records(self):
        """
        pulling records from
        merchant code & storing
        in database

        additional arguments can be
        added here

        :return: flag, message(success/err)
        """

        logger.debug("pull records (merchant_code): " + str(self.merchant_code))

        dataset = None

        # searching file startswith merchant_code
        # ie. merchant_name == merchant_code.lower()
        for i in os.listdir(data_dir):
            if i.startswith(self.merchant_code.lower()):
                data = json.load(open(os.path.join(data_dir, i), 'r'))
                dataset = data.get('products', None)
                break

        if dataset is None:
            return False, "No Data Available or merchant_code not found !"

        # calling bll to create objects in database
        result_message = ProductManager().create_product(dataset)

        logger.info(result_message)

        return True, result_message
