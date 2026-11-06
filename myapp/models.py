from django.db import models
from django.conf import settings


class Perfume(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    price_20ml = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    price_50ml = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )

    image_url = models.ImageField(
        upload_to='perfumes/', blank=True, null=True
    )
    image_20ml = models.ImageField(
        upload_to='perfumes/', blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name


class PerfumeImage(models.Model):
    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='perfumes/')

    def __str__(self):
        return self.perfume.name


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    pincode = models.CharField(max_length=10)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE
    )

    size = models.CharField(
        max_length=10,
        choices=[
            ('20ml', '20ml'),
            ('50ml', '50ml'),
        ],
        default='50ml'
    )

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order} - {self.perfume.name}"