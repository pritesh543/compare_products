from rest_framework import serializers
from products.models import Product, Review, Category

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["recommended_rank"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("category_name",)

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField('get_category_name')

    def get_category_name(self, product):
        return product.category_id.category_name

    class Meta:
        model = Product
        fields = [
            "id",
            "product_id",
            "product_name",
            "merchant_name",
            "listing_price",
            "sale_price",
            "discount",
            "brand",
            "description",
            "rating",
            "reviews",
            "url",
            "category_name"
        ]
