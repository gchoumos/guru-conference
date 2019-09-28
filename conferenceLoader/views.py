from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the conference index.")

def detect_guru(request):
    return HttpResponse("Guru Detector page will live here.")