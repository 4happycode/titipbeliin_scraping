from django import forms
from .models import ScrapingResult, ScrapingConfig

class ScrapingForm(forms.Form):
    config = forms.ModelChoiceField(queryset=ScrapingConfig.objects.all(), label='config', widget=forms.Select)
    link = forms.URLField(label='Link Of Product')

    def save(self):
        data = self.cleaned_data
        scrap = ScrapingResult(
            link=data['link'],
            scraping_config_id=data['config']
        )
        scrap.save()

        return scrap.custom_result()
    
    def update(self, data):
        id = data.get('id')
        scrap = ScrapingResult.objects.filter(pk=id).update(**data)
        return scrap

    class Meta:
        model = ScrapingResult