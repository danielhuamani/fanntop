from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required(login_url=reverse_lazy("web_system:login_register"))
def checkout_paso_1(request):
    ctx = {

    }
    return render(request, "order/checkout_1.html", ctx)

# Create your views here.
