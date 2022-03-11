from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from pprint import pprint

# Create your views here.


def home(request):
    pprint(dir(request))
    print(request.headers)
    return HttpResponse("hello")
