from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list_scraping, name='list scraping'),
    path('detail/<int:id>', views.detail_scraping, name='detail scraping'),
    path('create', views.create_scraping, name='create scraping'),
]