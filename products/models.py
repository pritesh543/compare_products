"""
Define you database here in
ORM mapping
easy to read and write
"""

from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=128)
    category_desc = models.CharField(max_length=256, null=False, blank=True)

class Product(models.Model):
    product_id = models.CharField(max_length=64)
    product_name = models.CharField(max_length=256)
    merchant_name = models.CharField(max_length=64)
    listing_price = models.FloatField(default=1.0)
    sale_price = models.FloatField(default=1.0)
    discount = models.FloatField(default=0)
    brand = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, default=None)
    reviews = models.CharField(max_length=1024, null=True, blank=True)
    url = models.CharField(max_length=512, null=True, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   to_field='id', related_name='product_review')
    recommended_rank = models.FloatField(default=0)
    comment = models.CharField(max_length=256, null=True, blank=True)
