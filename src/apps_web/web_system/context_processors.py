from apps_base.category.models import Category

def category_processors(request):
    categories = Category.objects.active().filter(category__isnull=True)
    ctx = {
        'categories_processors': categories
    }
    return ctx
