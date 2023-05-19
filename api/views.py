from django.shortcuts import render
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .serializers.RegisterSerializer import RegisterSerializer

# Create your views here.
@api_view(["GET","POST"])
def test(request, *args, **kwargs):
    return Response({'hehe':'papież tańczy'})

@api_view(['POST'])
def register(request, *args, **kwargs):
    serializer = RegisterSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response']="successfully registered a new user"
    else:
        data = serializer.errors
    return Response(data)


