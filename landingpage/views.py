from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache
def landingpage(request):
    return render(request, 'landingpage/index.html')
