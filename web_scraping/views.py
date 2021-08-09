from django.shortcuts import render
from django.http import HttpResponse

from .models import ScrapingResult


# Create your views here.
def index(request):
    return HttpResponse("Welcome")


def list_scraping(response):
    ls = ScrapingResult.objects.all().values()
    
    return render(response, "list.html", {"ls":list(ls)})