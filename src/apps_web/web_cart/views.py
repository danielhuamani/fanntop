from django.shortcuts import render

def cart(request):
    ctx = {}
    return render(request, 'cart/cart.html', ctx)