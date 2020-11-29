from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse

CATEGORY = (
    ('Shirt', 'Shirt'),
    ('Sport', 'Sport Wear'),
    ('Out wear', 'Out Wear')
)

BRAND = (
    ('AD', 'ADDIDAS'),
    ('FM', 'FAMOUS'),
    ('PX', 'PAPERLINX'),
    ('SE', 'SPOART ENGLAND'),
)

class ShippingAddress(models.Model):
    addr_line1 = models.TextField()
    addr_line2 = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=7)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.addr_line1


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_user')
    mobile_no = models.CharField(max_length=30)
    alternate_mobile_no = models.CharField(max_length=30)
    address = models.ManyToManyField(ShippingAddress)

    def __str__(self):
        return self.user_id.username


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    category = models.CharField(choices=CATEGORY, max_length=20)
    brand = models.CharField(choices=BRAND, max_length=2)
    description = models.TextField()
    image = models.ImageField(blank=True,upload_to='statics/image/')
    out_of_stock = models.BooleanField(default=False, help_text='if True : item is out of stock')

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("estoreapp:product", kwargs={
            "pk": self.pk
        })

    def get_add_to_cart_url(self):
        return reverse("estoreapp:add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("estoreapp:remove-from-cart", kwargs={
            "pk": self.pk
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
