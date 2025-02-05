# views.py
from django.shortcuts import render
from .models import Tovar

def product_list(request):
    products = Tovar.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = Tovar.objects.get(pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})
