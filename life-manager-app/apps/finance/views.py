from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .models import Wallet, Purchase
from django.db.models.functions import TruncMonth



@login_required
def home(request):
    wallets = Wallet.objects.all()
    purchases = Purchase.objects.annotate(month=TruncMonth('date')).order_by('-month')
    
    data = {}
    for purchase in purchases:
        month = purchase.month.strftime('%Y-%m')
        if month not in data:
            data[month] = {'wallets': [], 'purchases': []}
        if purchase.wallet not in data[month]['wallets']:
            data[month]['wallets'].append(purchase.wallet)
        data[month]['purchases'].append(purchase)
    context = {
        'data': data,
    }
    return render(request, 'finance/pages/home.html', context=context)


class MyLoginView(LoginView):
    template_name = 'finance/pages/login.html'

