from django.db import models
from django.db.models.enums import Choices

# Create your models here.
class ScrapingStatus(models.TextChoices):
    NEW     = 1, 'new'
    SUCCESS = 2, 'success'
    ERROR   = 3, 'error'

class ScrapingResult(models.Model):
    scraping_config_id = models.ForeignKey('ScrapingConfig', on_delete=models.CASCADE)
    link = models.URLField(blank=False, verbose_name="url product")
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    
    status = models.IntegerField(choices=ScrapingStatus.choices, default=ScrapingStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link
    
    def custom_result(self):
        respons = dict()
        respons['id'] = self.id
        respons['scraping_config_id'] = self.scraping_config_id
        respons['link'] = self.link
        return respons


class ImageResult(models.Model):
    scraping_result = models.ForeignKey('ScrapingResult', on_delete=models.CASCADE, default=None, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.image_url


class ResultChoices(models.TextChoices):
    NAME = 'name', 'get data name'
    PRICE = 'price', 'get data price'
    IMAGE = 'image_url', 'get data image'

class ScrapingConfig(models.Model):
    base_url = models.URLField(blank=False)

    def __str__(self):
        return self.base_url


class ScrapingConfigDetail(models.Model):
    scraping_config = models.ForeignKey('ScrapingConfig', on_delete=models.CASCADE, default=None, blank=True, null=True)
    taging = models.CharField(max_length=200)
    attribute_key = models.CharField(max_length=200)
    attribute_value = models.CharField(max_length=200)
    get_result = models.CharField(max_length=100, choices=ResultChoices.choices, default=None, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.scraping_config)
