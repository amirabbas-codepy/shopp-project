from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializers, ProductSerializer, SelectedProductsSerializer, CommentSerializer, FinalRegistraionSerializer
from django.db.models import Q, Sum
from .models import *
# Create your views here.

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    adress = request.data.get('adress')

    # data = UserSerializers(data=request.data)
    # print(data)
    if username and password:
        try:
            user = User(username=username, 
                        first_name=first_name, 
                        last_name=last_name, 
                        phone_number=phone_number, 
                        adress=adress)
            
            user.set_password(password)
            user.save()
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'mess':'success'}, status=status.HTTP_201_CREATED)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def send_all_products(request):
    product_serializer = ProductSerializer(Product.objects.filter(status=True), many=True)
    return Response(product_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def serch_products(request):
    value = request.data.get('value')
    print(value)
    if value:
        products = Product.objects.filter(Q(name__icontains = value) | Q(descripitions__icontains=value))
        if products:
            productsserializer = ProductSerializer(products, many=True)
            return Response(productsserializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'mess':'not found'}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_product(request):
    user = request.user
    idp = request.data.get('idp')
    count = request.data.get('count')
    print(count, idp, user)
    try:
        product = Product.objects.get(id=idp)
        count = int(count)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    check = SelectedPruduct.objects.filter(user=user, product=product)
    if check:
        shopingcart = check.first()
        shopingcart.count += count
        shopingcart.save()
        return Response(status=status.HTTP_200_OK)

    else:
        SelectedPruduct.objects.create(product=product, user=user, count=count)
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def proccess_shopping_cart(request):
    user = request.user

    shopping_cart = SelectedPruduct.objects.filter(user=user)
    if shopping_cart:
        final_price = 0
        for product in shopping_cart:
            final_price += product.product.price * product.count
        
        return Response({'final_price':final_price}, status=status.HTTP_200_OK)
    else:
        return Response({'mess':'سبد خرید خالی است'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    print(user)
    approval = request.data.get('approval')
    if approval:
        user.delete()
        return Response(status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_seleceted_products_in_shopping_card(request):
    idp = request.data.get('idp')
    user = request.user
    print(user)

    try:
        product = Product.objects.get(id=idp)
        s = SelectedPruduct.objects.get(user=user, product=product)
        
        s.count -= 1
        if s.count == 0:
            s.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            s.save()
            return Response({'count':s.count}, status=status.HTTP_200_OK)

    except:    
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def show_shopping_cart(request):
    user = request.user
    shopping_cart = SelectedPruduct.objects.filter(user=user)
    shopping_cart_serializers = SelectedProductsSerializer(shopping_cart, many=True)
    return Response(shopping_cart_serializers.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def final_shopping_cart_registarion(request):
    user = request.user

    shopping_cart = SelectedPruduct.objects.filter(user=user)
    if shopping_cart:
        final_price = 0
        for product in shopping_cart:
            final_price += product.product.price * product.count

        if user.balance >= final_price:
            for pr in shopping_cart:
                FinalRegistraion.objects.create(product=pr.product, user=user)
                SelectedPruduct.objects.filter(user=user).delete()
            
            user.balance -= final_price
            user.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'mess':'balance low'}, status=status.HTTP_402_PAYMENT_REQUIRED)
        
    return Response({'mess':'shopping cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request):
    idp = request.data.get('idp')
    text = request.data.get('text')
    user = request.user
    print(user)
    try:
        product = Product.objects.get(id=idp)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        if text:
            comment = {'des':text}
            cs = CommentSerializer(data=comment)
            if cs.is_valid():
                cs.save(user=user, product=product)
                return Response(status=status.HTTP_200_OK)
            else:
                print(cs.errors)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
def show_comments(request):
    idp = request.data.get('idp')

    try:
        product = Product.objects.get(id=idp)
        comments = Comment.objects.filter(product=product, status=True).order_by('-time_create')
    except:
        return Response({'mess':'not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    commentsserializer = CommentSerializer(comments, many=True)
    return Response(commentsserializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def show_final_registarions(request):
    user = request.user
    user_products = FinalRegistraion.objects.filter(user=user)
    user_products_serializers = FinalRegistraionSerializer(user_products, many=True)
    return Response(user_products_serializers.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def details_product(request, idp):
    try:
        product = Product.objects.get(id=idp)

    except:
        return Response({'mess':'not found'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        ps = ProductSerializer(product)
        return Response(ps.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({'user':request.user}, status=status.HTTP_200_OK)