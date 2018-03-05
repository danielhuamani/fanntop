from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from apps_base.pages.models import HomeBanner
from apps_base.influencer.models import Influencer
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .constants import REGISTER, LOGIN


def home(request):
    home_banners = HomeBanner.objects.active()
    influencers = Influencer.objects.active().order_by('position')
    ctx = {
        'home_banners': home_banners,
        'influencers': influencers
    }
    return render(request, "system/home.html", ctx)


def login_register(request):
    if request.method == 'POST':
        form_register = UserRegisterForm(prefix='register')
        form_login = AuthenticationForm(prefix='login')
        if request.POST.get('type_submit') == REGISTER:
            form_register = UserRegisterForm(request.POST, prefix='register')
            if form_register.is_valid():
                form_register.save()
                username = form_register.cleaned_data.get('username')
                raw_password = form_register.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect(reverse_lazy('web_system:account'))
        elif request.POST.get('type_submit') == LOGIN:
            form_login = AuthenticationForm(request, data=request.POST, prefix='login')
            if form_login.is_valid():
                auth_login(request, form_login.get_user())
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect(reverse_lazy('web_system:account'))
    else:
        form_register = UserRegisterForm(prefix='register')
        form_login = AuthenticationForm(prefix='login')
    ctx = {
        'form_register': form_register,
        'form_login': form_login,
        'LOGIN': LOGIN,
        'REGISTER': REGISTER
    }
    return render(request, "system/login_register.html", ctx)

@login_required(login_url=reverse_lazy("web_system:login_register"))
def account(request):

    ctx = {

    }
    return render(request, "system/account.html", ctx)