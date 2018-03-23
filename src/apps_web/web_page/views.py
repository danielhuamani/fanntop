from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ContactForm, ComplaintsBookForm
from apps_base.pages.models import FrequentQuestion, TermsConditions, PaymentMethods, Pages

def question(request):
    frequent_question, created = FrequentQuestion.objects.get_or_create(pk=1)
    ctx = {
        'frequent_question': frequent_question,
    }
    return render(request, "pages/frequent_question.html", ctx)

def terms_conditions(request):
    terms, created = FrequentQuestion.objects.get_or_create(pk=1)
    ctx = {
        'terms': terms,
    }
    return render(request, "pages/terms_conditions.html", ctx)

def payment_methods(request):
    payment, created = PaymentMethods.objects.get_or_create(pk=1)
    ctx = {
        'payment': payment,
    }
    return render(request, "pages/payment_methods.html", ctx)

def pages(request, slug):
    page = get_object_or_404(Pages, slug=slug)
    ctx = {
        'page': page
    }
    return render(request, "pages/page.html", ctx)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('web_page:contact_thanks'))
    else:
        form = ContactForm()
    ctx = {
        'form': form
    }
    return render(request, "pages/contact.html", ctx)


def contact_thanks(request):
    ctx = {
    }
    # if request.method == 'POST':
    # else:
    #     return redirect(reverse('web_system:home'))
    return render(request, "pages/contact_thanks.html", ctx)


def complaints_book(request):
    if request.method == 'POST':
        form = ComplaintsBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('web_page:contact_thanks'))
    else:
        form = ComplaintsBookForm()
    ctx = {
        'form': form
    }
    return render(request, "pages/complaints_book.html", ctx)