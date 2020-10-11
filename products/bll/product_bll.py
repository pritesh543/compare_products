# product business logic
from django.db.models import Q
from products.models import Product, Category

class ProductManager:
    def __init__(self):
        pass

    def get_product(self, product_id):
        try:
            return Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return None

    def validate_rating(self, rating):
        if type(rating) != int or type(rating) != float:
            return None
        else:
            return float(rating)

    def get_relevant_products(self, product_category, product_name):
        q = Q()
        q = q & Q(category_id__category_name__icontains=product_category)
        q = q & Q(product_name__icontains=product_name)

        products = Product.objects.filter(q)
        return products

    def get_category(self, category_name):
        """
        :category_name: category_name
        :rtype: object
        """
        category = Category.objects.filter(category_name__icontains=category_name)
        if category:
            return category[0]
        else:
            category_info = {"category_name": category_name}
            category = Category.objects.create(**category_info)
            return category

    def create_product(self, products):
        for product_info in products:
            product_info['category_id'] = self.get_category(product_info.get('category_name'))
            product_info['rating'] = self.validate_rating(product_info.get('rating'))
            product_info.pop('category_name')

        Product.objects.bulk_create([Product(**_product) for _product in products])

        return "%d record(s) inserted successfully" % (len(products))