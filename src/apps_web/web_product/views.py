from django.shortcuts import render, get_object_or_404
from apps_base.influencer.models import Influencer


def influencer_products(request, pk):
    influencer = get_object_or_404(Influencer, pk=pk)
    ctx = {
        'influencer': influencer
    }
    return render(request, 'product/influencer_list_products.html', ctx)
