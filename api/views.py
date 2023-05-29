from django.shortcuts import render
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from .serializers.RegisterSerializer import RegisterSerializer
from .serializers.RegisterCompanySerializer import RegisterCompanySerializer


# Create your views here.
@api_view(["GET","POST"])
def test(request, *args, **kwargs):
    return Response({'hehe':'papież tańczy'})


@api_view(['POST'])
def register(request, *args, **kwargs):
    serializer = RegisterSerializer(data=request.data)
    data = {}
    status_code = None
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = "successfully registered a new user"
        status_code=status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(data, status=status_code)


@api_view(['POST'])
def register_company(request, *args, **kwargs):
    serializer = RegisterCompanySerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = "successfully registered a new company"
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(data, status=status_code)
