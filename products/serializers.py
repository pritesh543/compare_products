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
    #product_set = ProductReviewSerializer(many=True)
    #category_id = serializers.SlugRelatedField(many=False, slug_field="id", read_only=True)
    #category_id = CategorySerializer()
    #category_id = serializers.CharField(source='products_set', read_only=True)

    category_name = serializers.SerializerMethodField('is_category')

    def is_category(self, product):
        return product.category_id.category_name

    class Meta:
        model = Product
        fields = [
            "id",
            "product_id",
            "product_name",
            "merchant_name",
            "category_name",
            "brand"
        ]

