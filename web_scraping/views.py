from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from asgiref.sync import sync_to_async

from .forms import ScrapingForm
from .models import ScrapingResult, ImageResult
from .helpers import ready_scraping, scraping
from django.forms.models import model_to_dict


# Create your views here.
def index(request):
    return HttpResponse("Welcome")


def list_scraping(response):
    ls = ScrapingResult.objects.all().values()
    
    return render(response, "list.html", {"ls":list(ls)})


def detail_scraping(response, id):
    ls = ScrapingResult.objects.filter(id=id).first()
    data = {'data': model_to_dict(ls)}

    images = ImageResult.objects.select_related('scraping_result').filter(scraping_result__id=id)
    data['images'] = list(images)

    # If use Join
    # d = ScrapingResult.objects.filter(imageresult__scraping_result=id).values('name', 'price', 'imageresult__image_url')
    
    return render(response, "detail.html", data)


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