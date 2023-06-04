from django.http import Http404
from django.shortcuts import render
import json
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404


from .serializers.RegisterSerializer import RegisterSerializer
from .serializers.RegisterCompanySerializer import RegisterCompanySerializer
from .serializers.CompanySerializer import CompanySerializer
from .serializers.MakeOpinionSerializer import MakeOpinionSerializer
from .serializers.SafeWordsSerializer import SafeWordsSerializer
from .serializers.CategoriesSerializer import CategoriesSerializer
from .models import Companies
from .models import Categories
from .models import CategoriesOfCompanies


# Create your views here.
@api_view(["GET", "POST"])
def test(request, *args, **kwargs):
    return Response({'hehe': 'papież tańczy'})


@api_view(['POST'])
def register(request, *args, **kwargs):
    serializer = RegisterSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data['response'] = "successfully registered a new user"
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(data, status=status_code)


@api_view(['POST', 'GET'])
def company(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(CategoriesOfCompanies, category_id=pk_categ, company_id=pk_comp)
            data = CompanySerializer(obj, many=False, context={'many': False}).data
            return Response(data)
        #qs = Companies.objects.filter(status="accepted")
        #data = CompanySerializer(qs, many=True, context={'many': True}).data
        #return Response(data)

    elif method == "POST":
        serializer = RegisterCompanySerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            api_url = "https://random-word-api.vercel.app/api?words=10&length=7";
            response = requests.get(api_url)
            if response.status_code != requests.codes.ok:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(data, status=status_code)
            json_response = json.loads(response.text)
            dictio = {}
            for index, word in enumerate(json_response, start=1):
                key = "word" + str(index)
                dictio[key] = word

            created_id = serializer.save()
            serializer2 = SafeWordsSerializer(data=dictio, context={'id': created_id.id})
            if serializer2.is_valid():
                serializer2.save()
                data['token'] = Companies.objects.filter(pk=created_id.id).values('token').first()['token']
                data['response'] = "Successfully registered a new company"
                data['responseWords'] = json_response
                status_code = status.HTTP_200_OK
                return Response(data, status=status_code)
            else:
                created_id.delete()
        data = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


@api_view(['POST'])
def opinion(request, *arg, **kwargs):
    data = {}
    if not request.user.is_authenticated:
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    serializer = MakeOpinionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        data['response'] = "successfully added a new opinion"
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(data, status=status_code)


@api_view(['GET'])
def categories(request, pk=None, *arg, **kwargs):
    paginator = LimitOffsetPagination()
    if pk is None:
        category = Categories.objects.all()
        paginated_category = paginator.paginate_queryset(category, request)
        paginated_data = CategoriesSerializer(paginated_category, many=True)
    else:
        categories_of_companies = CategoriesOfCompanies.objects.select_related('company').filter(category_id=pk)
        if not categories_of_companies.exists():
            raise Http404
        company_ids = [category_of_company.company.id for category_of_company in categories_of_companies]
        paginated_companies = paginator.paginate_queryset(company_ids, request)
        companies = Companies.objects.filter(pk__in=paginated_companies)
        paginated_data = CompanySerializer(companies, many=True)
    return paginator.get_paginated_response(paginated_data.data)


@api_view(['GET'])
def category_pagable(request, amount=6, *arg, **kwargs):
    data = {'countAll': Categories.objects.count(),
            'countAllPages': (-(-Categories.objects.count() // amount))}
    return Response(data, status=status.HTTP_200_OK)
