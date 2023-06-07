from django.http import Http404
import json
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count, Case, When, Subquery, F

from .serializers.RegisterSerializer import RegisterSerializer
from .serializers.RegisterCompanySerializer import RegisterCompanySerializer
from .serializers.CompanySerializer import CompanySerializer
from .serializers.MakeOpinionSerializer import MakeOpinionSerializer
from .serializers.SafeWordsSerializer import SafeWordsSerializer
from .serializers.CategoriesSerializer import CategoriesSerializer
from .serializers.LoginSerializer import LoginSerializer
from .serializers.LoginCompanySerializer import LoginCompanySerializer
from .serializers.RefreshSerializer import RefreshSerializer
from .serializers.ResetTokenSerializer import ResetTokenSerializer
from .models import Companies
from .models import Categories
from .models import CategoriesOfCompanies
from .utils.generate_safe_words import generate_safe_words
from .utils.generate_safe_words import make_dictio
from api.utils.companies_filtr_sort import companies_sorting_filtring


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


@api_view(['POST'])
def login(request, *args, **kwargs):
    serializer = LoginSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        data = serializer.data
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=status_code)

@api_view(['POST'])
def login_company(request, *args, **kwarg):
    serializer = LoginCompanySerializer(data=request.data)
    data={}
    if serializer.is_valid():
        data = serializer.data
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=status_code)


@api_view(['POST', 'GET'])
def company(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET" and pk is not None:
        obj = get_object_or_404(Companies, pk=pk, status="accepted")
        data = CompanySerializer(obj, many=False, context={'request': request}).data
        return Response(data)

    elif method == "POST":
        serializer = RegisterCompanySerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            json_response = generate_safe_words()
            if json_response is None:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(data, status=status_code)

            created_id = serializer.save()
            serializer2 = SafeWordsSerializer(data=make_dictio(json_response), context={'id': created_id.id})
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


@api_view(['POST'])
def categories(request, *arg, **kwargs):
    pk = request.query_params["category"]
    paginator = LimitOffsetPagination()

    if pk is None or pk == "":
        category = Categories.objects.all()
        paginated_category = paginator.paginate_queryset(category, request)
        paginated_data = CategoriesSerializer(paginated_category, many=True)
        return paginator.get_paginated_response(paginated_data.data)

    if not Categories.objects.filter(pk=pk).exists():
        raise Http404
    categories_of_companies = CategoriesOfCompanies.objects.select_related('company').filter(category_id=pk)
    company_ids = [category_of_company.company.id for category_of_company in categories_of_companies]

    avg_grade = request.data.get('avgGrade')
    sort_by = request.data.get('sortBy')
    sort_dir = request.data.get('sortDir')
    has_grades = request.data.get('hasGrades')

    results = companies_sorting_filtring(avg_grade, sort_by, sort_dir, has_grades)
    results = results.filter(pk__in=company_ids)
    paginated_companies = paginator.paginate_queryset(results, request)
    paginated_data = CompanySerializer(paginated_companies, many=True)
    response = paginator.get_paginated_response(paginated_data.data)
    response.data['category'] = Categories.objects.filter(pk=pk).first().name

    return Response(data=response.data)


@api_view(['GET'])
def category_pageable(request, amount=6, *arg, **kwargs):
    data = {'countAll': Categories.objects.count(),
            'countAllPages': (-(-Categories.objects.count() // amount))}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def company_pageable(request, amount=6, *arg, **kwargs):
    query = request.GET.get("query")
    if query is not None or query != "":
        companies = Companies.objects.filter(Q(name__icontains=query) & Q(status="accepted"))
    else:
        companies = Companies.objects.filter(status="accepted")

    data = {'countAll': companies.count(),
            'countAllPages': (-(-companies.count() // amount))}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def company_category_pageable(request, pk=None, amount=6, *arg, **kwargs):
    if pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    categories_of_companies = CategoriesOfCompanies.objects.select_related('company').filter(category_id=pk)
    company_ids = [category_of_company.company.id for category_of_company in categories_of_companies]
    companies = Companies.objects.filter(pk__in=company_ids)

    data = {'countAll': companies.count(),
            'countAllPages': (-(-companies.count() // amount))}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def refresh_token(request, *arg, **kwargs):
    serializer = RefreshSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        data['access'] = serializer.data['access']
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=status_code)


@api_view(['POST'])
def search_companies(request, *arg, **kwargs):
    query = request.query_params["query"]
    paginator = LimitOffsetPagination()

    avg_grade = request.data.get('avgGrade')
    sort_by = request.data.get('sortBy')
    sort_dir = request.data.get('sortDir')
    has_grades = request.data.get('hasGrades')

    results = companies_sorting_filtring(avg_grade, sort_by, sort_dir, has_grades, query)

    paginated_companies = paginator.paginate_queryset(results, request)
    response_results = CompanySerializer(paginated_companies, many=True)
    return paginator.get_paginated_response(response_results.data)


@api_view(['POST'])
def reset_token(request, *arg, **kwargs):
    serializer = ResetTokenSerializer()
    test = serializer.check_words(data=request.data)
    message = test
    status_code = status.HTTP_200_OK

    return Response(message, status=status_code)

