from django.db import models
from django.contrib.auth.models import AbstractUser
import django_jalali.db.models as jmodels
# Create your models here.

class User(AbstractUser):
    balance = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=11, null=True, unique=True)
    adress = models.TextField(null=True)

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    cat = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='another')
    price = models.IntegerField()
    pic = models.FileField(upload_to='./media/shoponline', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descripitions = models.TextField()
    brand = models.CharField(max_length=200, null=True)
    time_create = jmodels.jDateTimeField(auto_now_add=True)
    time_update = jmodels.jDateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    des = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time_create = jmodels.jDateTimeField(auto_now_add=True)
    time_update = jmodels.jDateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class SelectedPruduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

class FinalRegistraion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    time_create = jmodels.jDateTimeField(auto_now_add=True)
    time_update = jmodels.jDateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    count = models.IntegerField(null=True)