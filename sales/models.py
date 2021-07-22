from django.db import models
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from .utils import generate_transaction_id
from django.shortcuts import reverse

# Create your models here.
# Position is Product * quantity -> price
class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # price is automatic by overriding save method to set it as product.price * quantity
    price = models.FloatField(blank=True)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        # set creation date
        if self.created_at is None:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def get_sales(self):
        sales_list = self.sale_set.all()
        return sales_list

    def __str__(self) -> str:
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"
    
# Sale is comprised of many Positions
class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        # generate transaction_id code
        if self.transaction_id == "":
            self.transaction_id =  generate_transaction_id()
        # set creation date
        if self.created_at is None:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Sales for the amount of €{self.total_price}"

    def get_absolute_url(self):
        return reverse("sales:detail", kwargs={"pk": self.pk})
        
    def get_positions(self):
        return self.positions.all()

class CSV(models.Model):
    file_name = models.FileField(upload_to='csvs')
    activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.file_name)