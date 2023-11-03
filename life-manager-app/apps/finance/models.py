from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')

class Purchase(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='purchases')
