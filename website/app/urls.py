from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('find', views.find, name='find'),
    path('find_list', views.find_list, name='find_list'),
]