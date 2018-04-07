from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ContactForm, ComplaintsBookForm
from apps_base.form.models import  ComplaintsBook
from apps_base.pages.models import FrequentQuestionResponse, TermsConditions, PaymentMethods, Pages


# def terms_conditions(request):
#     terms, created = FrequentQuestion.objects.get_or_create(pk=1)
#     ctx = {
#         'terms': terms,
#     }
#     return render(request, "pages/terms_conditions.html", ctx)

def question_response(request):
    question_responses = FrequentQuestionResponse.objects.filter(
        is_active=True).order_by('position')
    question_response_first = ''
    if question_responses.exists():
        question_response_first = question_responses.first()
    ctx = {
        'question_responses': question_responses,
        'question_response_first': question_response_first
    }
    return render(request, "pages/question_response.html", ctx)


def question_response_question(request, slug):
    question_response = get_object_or_404(FrequentQuestionResponse, slug=slug, is_active=True)
    question_responses = FrequentQuestionResponse.objects.filter(
        is_active=True).order_by('position')
    ctx = {
        'question_response': question_response,
        'question_responses': question_responses,
    }
    return render(request, "pages/question_response_question.html", ctx)

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
            complaints_book_generate = form.save()
            return redirect(reverse(
                'web_page:complaints_book_generate',
                kwargs={'uuid_hash': complaints_book_generate.uuid}))
    else:
        form = ComplaintsBookForm()
    ctx = {
        'form': form
    }
    return render(request, "pages/complaints_book.html", ctx)


def complaints_book_generate(request, uuid_hash):
    complaints = get_object_or_404(ComplaintsBook, uuid=uuid_hash)

    ctx = {
        'complaints': complaints
    }
    return render(request, "pages/complaints_book_generate.html", ctx)