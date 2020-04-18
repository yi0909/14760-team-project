from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('find', views.find, name='find'),
    path('find_list', views.find_list, name='find_list'),
    path('find_stop', views.find_stop, name='find_stop'),
    path('receive', views.receive, name='receive'),
    path('receive_stop', views.receive_close, name='receive_close'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('upload_dir', views.upload_dir, name='upload_dir'),
]