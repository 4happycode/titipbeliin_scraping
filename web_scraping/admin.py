from django.contrib import admin
from django.db import models
from .models import ScrapingConfig, ScrapingResult, ScrapingConfigDetail, ImageResult

# Register your models here.
class ScrapingConfigDetailInline(admin.StackedInline):
    model = ScrapingConfigDetail
    extra = 3
    max_num = 3

class ScrapingConfigAdmin(admin.ModelAdmin):
    inlines = [ScrapingConfigDetailInline,]

admin.site.register(ScrapingConfig, ScrapingConfigAdmin)


class ImageResultInline(admin.StackedInline):
    model = ImageResult
    extra = 0

class ScrapingResultAdmin(admin.ModelAdmin):
    inlines = [ImageResultInline,]

    # Cannot add from admin
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(ScrapingResult, ScrapingResultAdmin)
