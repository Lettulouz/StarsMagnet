from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def example_view(request):
    return render(request, 'testTemplate.html')