from django.urls import path
from .views import index, redirect_urls
from core import views

urlpatterns = [
    path('', index, name='index'),

    path('<slug>/', views.special_links, name='special_links'),

]
