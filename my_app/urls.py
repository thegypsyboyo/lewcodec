from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('new_search', views.new_search, name='new_search'),
]


