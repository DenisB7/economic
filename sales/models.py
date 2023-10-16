from django.db import models
from django.contrib.auth import get_user_model


class Sale(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=100)
    sales_number = models.IntegerField()
    revenue = models.DecimalField(max_digits=10, decimal_places=3)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.product
