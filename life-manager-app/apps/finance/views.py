from collections import OrderedDict
from itertools import groupby
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Purchase, Wallet


class PurchaseListView(TemplateView):
    template_name = 'finance/pages/purchases-by-month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = Purchase.objects.annotate(month=TruncMonth('date')).order_by('month')
        
        # Group by month using itertools.groupby
        grouped_purchases = OrderedDict()
        for key, group in groupby(purchases, key=attrgetter('month')):
            grouped_purchases[key] = list(group)

        context['grouped_purchases'] = grouped_purchases
        return context



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

