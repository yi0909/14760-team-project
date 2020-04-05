from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import loader


def index(request):
    return render_to_response("index.html")