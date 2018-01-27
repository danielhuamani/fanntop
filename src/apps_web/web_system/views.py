from django.shortcuts import render
from apps_base.pages.models import HomeBanner
from apps_base.influencer.models import Influencer

# Create your views here.
def home(request):
    home_banners = HomeBanner.objects.active()
    influencers = Influencer.objects.active().order_by('position')
    ctx = {
        'home_banners': home_banners,
        'influencers': influencers
    }
    return render(request, "system/home.html", ctx)
