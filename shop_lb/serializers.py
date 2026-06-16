from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Getter
        fields = '__all__'

class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = '__all__'

class Bucket_ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket_Element
        fields = '__all__'