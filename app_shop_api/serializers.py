
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import User, Product, Category, Comment, SelectedPruduct, FinalRegistraion

class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','cat','price','pic', 'descripitions','brand', 'time_create']

class SelectedProductsSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = SelectedPruduct
        fields = ['count', 'product']
        # depth = 1

class FinalRegistraionSerializer(ModelSerializer):
    # selecteds =PrimaryKeyRelatedField(queryset=SelectedPruduct.objects.all(), many=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = FinalRegistraion
        fields = ['id', 'time_create', 'product', 'status']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'time_create', 'des']
