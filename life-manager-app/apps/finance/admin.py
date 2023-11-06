from django import forms
from django.contrib import admin

from .models import Purchase, Wallet

admin.site.register(Wallet)
admin.site.register(Purchase)
