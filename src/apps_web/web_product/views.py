from django.shortcuts import render, get_object_or_404
from apps_base.influencer.models import Influencer
from apps_base.category.models import Category
from apps_base.product.models import Product, ProductClass


def influencer_products(request, slug):
    influencer = get_object_or_404(Influencer, slug=slug)

    ctx = {
        'influencer': influencer
    }
    return render(request, 'product/influencer_list_products.html', ctx)

def influencer_products_new(request, slug):
    influencer = get_object_or_404(Influencer, slug=slug)

    ctx = {
        'influencer': influencer
    }
    return render(request, 'product/influencer_list_products_new.html', ctx)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    ctx = {
        'category': category
    }
    return render(request, 'product/category_list_products.html', ctx)


def category_child_products(request, slug, slug_child):
    category = get_object_or_404(Category, category__slug=slug, slug=slug_child)
    ctx = {
        'category': category
    }
    return render(request, 'product/category_list_products.html', ctx)


def product(request, slug):
    product = get_object_or_404(ProductClass, slug=slug)
    ctx = {
        'product': product
    }
    return render(request, 'product/product.html', ctx)


def product_favorites(request):
    ctx = {}
    return render(request, 'product/product_favorites.html', ctx)

def product_search(request):
    ctx = {
        'search': request.GET.get('search')
    }
    return render(request, 'product/product_search.html', ctx)