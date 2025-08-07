from django.shortcuts import render, redirect
from app_shop_api.models import Comment, User, Product, FinalRegistraion, SelectedPruduct
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import *
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect(home_view)
    if request.method == 'POST':
        form_data = LoginForm(request.POST)
        if form_data.is_valid():
            data = form_data.cleaned_data
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                login(request=request, user=user)
                return redirect(home_view)
            else:
                messages.error(request=request, message='Invalid User')
                return render(request=request, template_name='login.html', context={'form':LoginForm()})
        else:
            messages.error(request=request, message='Data Error')
            return render(request=request, template_name='login.html', context={'form':LoginForm()})

    return render(request=request, template_name='login.html', context={'form':LoginForm()})

def register(request):
    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            data = form_data.cleaned_data
            username = data.get('username')
            password = data.get('password')
            phone_number = data.get('phone_number')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            adress = data.get('adress')

            try:
                user = User(username=username, 
                            first_name=first_name, 
                            last_name=last_name, 
                            phone_number=phone_number, 
                            adress=adress)
                
                user.set_password(password)
                user.save()
            except:
                messages.error(request=request, message='Change The Informations')
                return render(request=request, template_name='register.html', context={'form':RegisterForm()})

            else:
                return redirect(login_view)
        else:
            messages.error(request=request, message='Server Error (Input Data Erorr)')
            return render(request=request, template_name='register.html', context={'form':RegisterForm()})
            
    return render(request=request, template_name='register.html', context={'form':RegisterForm()})

def home_view(request):
    res = Product.objects.filter(status=True)
    return render(request=request, template_name='home.html', context={'products':res, 'sf':SerchForm()})

@login_required(login_url='/shoptemp/logintemp/')
def logout_view(request):
    logout(request=request)
    return redirect(login_view)

def details(request, idp):
    try:
        product = Product.objects.get(id=idp, status=True)

    except:
        messages.error(request=request, message='Product Not Found')
        return redirect(home_view)
    else:
        return render(request=request, template_name='details.html', context={'product':product, 'form':CommentForm()})

@login_required(login_url='/shoptemp/logintemp/')
def seletc_product_view(request, idp2):
    user = request.user
    print(idp2)
    try:
        product = Product.objects.get(id=idp2)
        
    except:
        messages.error(request=request, message='محصول یافت نشد')
        return redirect(home_view)
    
    check = SelectedPruduct.objects.filter(user=user, product=product)
    if check:
        shopingcart = check.first()
        shopingcart.count += 1
        shopingcart.save()
        messages.success(request=request, message='به سبد خرید اضافه شد')
        return redirect(shopping_cart)

    else:
        SelectedPruduct.objects.create(product=product, user=user, count=1)
        messages.success(request=request, message='به سبد خرید افزوده شد')
        return redirect(shopping_cart) 

@login_required(login_url='/shoptemp/logintemp/')
def profile(request):
    return render(request=request, template_name='profile.html', context={'user':request.user, 'balance':f'{request.user.balance:,}'}) 

@login_required(login_url='/shoptemp/logintemp/')
def shopping_cart(request):
    shopping_carts = SelectedPruduct.objects.filter(user=request.user)
    final_price = 0
    if shopping_carts:
        for product in shopping_carts:
            final_price += product.product.price * product.count
    
    return render(request=request, template_name='shopingcart.html', context={'user':request.user, 
                                                                          'shoppingcart':shopping_carts, 
                                                                          'price':f'{final_price:,}', 
                                                                          'balance':f'{request.user.balance:,}'})

def comment_view(request, idp3):
    user = request.user
    print(user)
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=idp3)
        except:
            messages.error(request=request, message='Product Not Found')
            return redirect(home_view)
        else:
            form_data = CommentForm(request.POST)
            if form_data.is_valid():
                data = form_data.cleaned_data
                comment = data.get('comment')
                Comment.objects.create(user=user, des=comment, product=product)
            
            else:
                messages.error(request=request, message='Data Input Error')
                return redirect(home_view)
            
        messages.success(request=request, message='نظر شما ثبت شد')
        return redirect(home_view)
    
    return render(request=request, template_name='details.html', context={'form':CommentForm()})

def show_comments(request, idp4):
    try:
        product = Product.objects.get(id=idp4)
    except:
        messages.error(request=request, message='Product Not Found')
        return redirect(home_view)
    else:
        comments = Comment.objects.filter(product=product, status=True)
        return render(request=request, template_name='comments.html', context={'com':comments})
    
def delete_selected_product(request, idp5):
    user = request.user
    print(user)

    try:
        product = Product.objects.get(id=idp5)
        shopping_carts = SelectedPruduct.objects.get(user=user, product=product)
        
        shopping_carts.count -= 1
        if shopping_carts.count == 0:
            shopping_carts.delete()
            return redirect(shopping_cart)
        else:
            shopping_carts.save()
            return redirect(shopping_cart)

    except:   
        messages.error(request=request, message='وجود ندارد') 
        return redirect(shopping_cart)

def serch_product(request):
    if request.method == 'POST':
        form_data = SerchForm(request.POST)
        if form_data.is_valid():
            data = form_data.cleaned_data
            value = data.get('value')

            if not value:
                return redirect(home_view)
            else:
                products = Product.objects.filter(Q(name__icontains=value) | Q(brand__icontains=value))
                if products:
                    return render(request=request, template_name='home.html', context={'products':products})
                else:
                    messages.error(request=request, message='کالا مورد نظر یافت نشد')
                    return redirect(home_view) 
    return redirect(home_view)

def final_shopping_cart_registarion(request):
    if request.method == 'POST':
        user = request.user

        shopping_carts = SelectedPruduct.objects.filter(user=user)
        if shopping_carts:
            final_price = 0
            for product in shopping_carts:
                final_price += product.product.price * product.count

            if user.balance >= final_price:
                for pr in shopping_carts:
                    FinalRegistraion.objects.create(product=pr.product, user=user)
                SelectedPruduct.objects.filter(user=user).delete()
                
                user.balance -= final_price
                user.save()

                return redirect(profile)
            else:
                messages.error(request=request, message='موجودی کافی نیست')
                return redirect(shopping_cart)
        messages.error(request=request, message='سبد خرید خالی است')
        return redirect(shopping_cart)
    return redirect(home_view)