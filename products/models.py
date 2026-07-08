from django.db import models
from categories.models import Category


class Product(models.Model):
    UNIT_CHOICES = (
        ('PCS', 'PCS'),
        ('KG', 'KG'),
        ('LTR', 'LTR'),
        ('BOX', 'BOX'),
    )

    product_code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=150)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    barcode = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    minimum_stock = models.PositiveIntegerField(default=5)

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='PCS'
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['product_name']

    def __str__(self):
        return self.product_name

    @property
    def low_stock(self):
        return self.stock <= self.minimum_stock