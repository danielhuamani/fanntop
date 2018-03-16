from django.shortcuts import render, get_object_or_404
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