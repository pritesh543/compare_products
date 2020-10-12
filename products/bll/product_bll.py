"""
This is a ``business logic layer``
where only logic presents
and encapsulation
"""

from django.db.models import Q
from products.models import Product, Category
from common.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)
logger.info("product-bll....")

class ProductManager:
    """
    This class handles the
    logic methods
    invoked by views (web/api)
    """
    def __init__(self):
        pass

    def get_product(self, product_id):
        """
        Returns the product object
        if found in database

        :param product_id:
        :return: object or None
        """
        try:
            return Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return None

    def validate_rating(self, rating):
        """
        Validates the rating
        specially type & strict typing

        :param rating:
        :return: float(rating) or None
        """
        if type(rating) != int or type(rating) != float:
            return None
        else:
            return float(rating)

    def get_relevant_products(self, product_category, product_name):
        """
        This function returns
        the list of products
        on product_name & category filers

        :param product_category:
        :param product_name:
        :return:
        """
        # regex match on name & category
        # __icontains is equals to -> %string%
        # inner join below

        q = Q()
        q = q & Q(category_id__category_name__icontains=product_category)
        q = q & Q(product_name__icontains=product_name)

        logger.debug(str(q))

        products = Product.objects.filter(q)
        return products

    def get_category(self, category_name):
        """
        Returns the category object
        if found or creates a new in database

        :category_name: category_name
        :rtype: object
        """
        logger.info("category_name: " + str(category_name))

        category = Category.objects.filter(category_name__icontains=category_name)
        if category:
            return category[0]
        else:
            category_info = {"category_name": category_name}
            category = Category.objects.create(**category_info)
            return category

    def check_file_extension(self, file_name):
        """
        extract the file extension
        and validates it

        :param file_name:
        :return: message
        """
        if file_name.split(".")[-1] in ['csv', 'xlsx']:
            return True, "file supported"
        else:
            return False, "only `csv` or `xlsx` supported as of now."

    def create_product(self, products):
        """
        Creating database objects in bulk
        on validated data

        :param products:
        :return: message(success/error)
        """

        for product_info in products:
            product_info['category_id'] = self.get_category(product_info.get('category_name'))
            product_info['rating'] = self.validate_rating(product_info.get('rating'))
            product_info.pop('category_name')

        # bulk creation of objects here
        Product.objects.bulk_create([Product(**_product) for _product in products])

        logger.info("create products: objects created successfully !")

        return "%d record(s) inserted successfully" % (len(products))
