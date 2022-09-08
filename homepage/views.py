from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'homepage/index.html', {})
def homepage(request):
    return render(request, 'homepage/homepage.html', {})
