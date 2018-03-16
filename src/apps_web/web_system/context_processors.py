from apps_base.category.models import Category
from apps_base.influencer.models import Influencer
from apps_base.pages.models import Pages

def category_processors(request):
    categories = Category.objects.active().filter(category__isnull=True).prefetch_related('category_categories')
    influencers = Influencer.objects.active().order_by('position')
    ctx = {
        'categories_processors': categories,
        'influencers_processors': influencers
    }
    return ctx

def pages_processors(request):
    pages = Pages.objects.active().order_by('position')
    ctx = {
        'pages_processors': pages
    }
    return ctx