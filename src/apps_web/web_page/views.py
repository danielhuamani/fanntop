from django.shortcuts import render
from apps_base.pages.models import FrequentQuestion

def question(request):
    frequent_question, created = FrequentQuestion.objects.get_or_create(pk=1)
    ctx = {
        'frequent_question': frequent_question,
    }
    return render(request, "pages/frequent_question.html", ctx)