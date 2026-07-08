from django.db import models


class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('Regular', 'Regular'),
        ('Wholesale', 'Wholesale'),
        ('Retail', 'Retail'),
    )

    customer_code = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=150)
    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPES,
        default='Regular'
    )

    company_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Pakistan')

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['customer_name']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.customer_code} - {self.customer_name}"