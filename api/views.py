from django.shortcuts import render
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET","POST"])
def test(request, *args, **kwargs):
    return Response({'hehe':'papież tańczy'})
