from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from asgiref.sync import sync_to_async

from .forms import ScrapingForm
from .models import ScrapingResult
from .helpers import ready_scraping, scraping


# Create your views here.
def index(request):
    return HttpResponse("Welcome")


def list_scraping(response):
    ls = ScrapingResult.objects.all().values()
    
    return render(response, "list.html", {"ls":list(ls)})


def create_scraping(response):
    if response.method == "POST":
        f = ScrapingForm(response.POST)
        if f.is_valid():
            saving = f.save()
            # sync_to_async(ready_scraping(saving), thread_sensitive=False)
            scraping(saving)._process()
            return HttpResponseRedirect('/list')
    else:
        f = ScrapingForm()
    return render(response, "create.html", {"form": f})