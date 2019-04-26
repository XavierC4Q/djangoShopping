from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from .choices import (
    STATES,
    GENDER,
    PRODUCT_TYPES,
    AGE_RANGE,
    SEASONS,
    SUB_CATEGORY
)
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    display_name = models.CharField(
        max_length=14,
        null=False,
        blank=False,
        validators=[MinLengthValidator(6, 'Display name must be at least 6 characters')]
    )
    state = models.CharField(max_length=32, choices=STATES)
    email = models.EmailField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.display_name


class Product(models.Model):
    name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        validators=[MinLengthValidator(10)]
    )
    gender = models.CharField(max_length=6, choices=GENDER)
    season = models.CharField(max_length=6, choices=SEASONS)
    age = models.CharField(max_length=5, choices=AGE_RANGE)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    price = models.FloatField()
    supplier = models.CharField(max_length=100, blank=False, null=False)


    def __str__(self):
        return self.name

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, default='')
    sub_category = models.CharField(max_length=20, choices=SUB_CATEGORY)
    sizes = ArrayField(
        models.CharField(max_length=4, blank=False, null=False),
        blank=False,
        null=False
    )
    colors = ArrayField(
        models.CharField(max_length=20, blank=False, null=False),
        blank=False,
        null=False
    )

    def __str__(self):
        return f'{self.product.name} Details'


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    items = models.ManyToManyField(Product, related_name='Product')

    def __str__(self):
        return f'Order #{self.id} by {self.user.display_name}'