from django.http import Http404

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers

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
from .serializers.CompanyOpinionSerializer import CompanyOpinionSerializer
from .serializers.OpinionSerializer import OpinionSerializer
from .models import Companies
from .models import Categories, Opinions
from .models import CategoriesOfCompanies
from .utils.generate_safe_words import generate_safe_words
from .utils.generate_safe_words import make_dictio
from api.utils.companies_filtr_sort import companies_sorting_filtring
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.


@api_view(['POST'])
def register(request, *args, **kwargs):
    """
    View function to register new user.
    :param request: HttpRequest object.
    :param args: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: response with success status code if user successfully register, otherwise
    error code with details.
    """
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
    """
    View used to log in by users.
    :param HttpRequest request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns jwt and user data with success status code or
    error status code with details.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.data
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=status_code)


@api_view(['POST'])
def login_company(request, *args, **kwarg):
    """
    View used to log in by companies.
    :param HttpRequest request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns jwt and company data with success status code or
    error status code with details.
    """
    serializer = LoginCompanySerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.data
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=status_code)


@api_view(['POST', 'GET'])
def company(request, pk=None, *args, **kwargs):
    """
    View function to handle GET and POST requests related to creating companies and displaying a specific company.
    :param request: HttpRequest object.
    :param pk: Primary key of the company (optional).
    :param args: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: For the GET method, the function returns the data of the company with the specified primary key or an error
     code. The POST method returns the company's token, a list of words used to reset the password,
     a message that the user has successfully registered, and an HTTP code.
    """
    method = request.method

    if method == "GET" and pk is not None:
        obj = get_object_or_404(Companies, pk=pk, status="accepted")
        data = CompanySerializer(obj, many=False).data
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
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = MakeOpinionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        new_opinion = serializer.save()
        opinion_serializer = OpinionSerializer(instance=new_opinion)
        data['response'] = "Successfully added a new opinion."
        data['new_opinion'] = opinion_serializer.data
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(data, status=status_code)


@api_view(['GET'])
def list_company_opinions(request, company_id,  *arg, **kwargs):
    """
    List opinions associated with a specific company.
    :param request: HttpRequest object.
    :param company_id: Identifier of the company for which opinions should be returned.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Response with list of opinions with pagination and HTTP code
    """
    data = {}
    opinions = Opinions.objects.filter(company_id=company_id)
    if opinions is None:
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(status=status_code)
    else:
        paginator = LimitOffsetPagination()
        data = OpinionSerializer(instance=opinions, many=True).data
        status_code = status.HTTP_200_OK

        paginated_opinions = paginator.paginate_queryset(data, request)
        response = paginator.get_paginated_response(paginated_opinions)

        return Response(data=response.data, status=status_code)


@api_view(['GET'])
def company_opinions_pageable(request, company_id,  *arg, **kwargs):
    """
    Data used to set pagination values for the list of reviews of a specific company
    :param request: HttpRequest object.
    :param company_id: Identifier of the company for which results should be returned.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return:It returns for a given company the number of reviews and how many reviews will fit on a single page.
    In addition, it returns the HTTP code
    """
    amount = request.query_params["fixedLimit"]
    try:
        amount = int(amount)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    opinions = Opinions.objects.filter(company_id=company_id).count()
    data = {'countAll': opinions,
            'countAllPages': (-(-opinions // amount))}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def company_opinion(request, *arg, **kwargs):
    data = {}
    if not request.user.is_authenticated:
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = CompanyOpinionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        new_opinion = serializer.save()
        opinion_serializer = OpinionSerializer(instance=new_opinion)
        data['response'] = "Successfully replay to opinion."
        data['newOpinion'] = opinion_serializer.data
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(data, status=status_code)


@api_view(['GET'])
def categories(request, *arg, **kwargs):
    """
    List of all categories.
    :param request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns a list of all available categories with pagination.
    """
    paginator = LimitOffsetPagination()
    category = Categories.objects.all()
    paginated_category = paginator.paginate_queryset(category, request)
    paginated_data = CategoriesSerializer(paginated_category, many=True)
    return paginator.get_paginated_response(paginated_data.data)


@api_view(['GET'])
def categories_list(request, *arg, **kwargs):
    """
    A list of categories consisting only of identifiers and names.
    :param request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns a list of identifiers and names of all available categories.
    """
    category = Categories.objects.all().values('id', 'name')
    return Response(category)


@api_view(['POST'])
def companies_of_category(request, *arg, **kwargs):
    """
    List of companies of a given category with the possibility of sorting and filtering
    :param request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns a filtered and sorted list of companies with a given category and HTTP code
    """
    pk = request.query_params["category"]
    paginator = LimitOffsetPagination()

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
    """
    Data used to set pagination values for the list of categories
    :param request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return:It returns the number of categories and how many categories will fit on a single page.
    In addition, it returns the HTTP code
    """
    data = {'countAll': Categories.objects.count(),
            'countAllPages': (-(-Categories.objects.count() // amount))}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def company_pageable(request, *arg, **kwargs):
    """
    Data used to set pagination values for the list of companies
    :param HttpRequest request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns the number of companies and how many companies will fit on one page using the fixedLimit and
    the search phrase passed by the query param. In addition, it returns the HTTP code.
    """
    query = request.GET.get("query")
    amount = request.query_params["fixedLimit"]

    try:
        amount = int(amount)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    avg_grade = request.data.get('avgGrade')
    sort_by = request.data.get('sortBy')
    sort_dir = request.data.get('sortDir')
    has_grades = request.data.get('hasGrades')

    if query is not None or bool(query):
        results = companies_sorting_filtring(avg_grade, sort_by, sort_dir, has_grades)
        companies = results.filter(Q(name__icontains=query))
    else:
        companies = Companies.objects.filter(status="accepted")

    data = {'countAll': companies.count(),
            'countAllPages': (-(-companies.count() // amount))}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def company_category_pageable(request, *arg, **kwargs):
    """
    Data used to set pagination values for the list of companies of specific category
    :param HttpRequest request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns the number of companies of a given category and how many of them will fit on one page using
    fixedLimit and amount passed by the query parameter. In addition, it returns the HTTP code.
    """
    category = request.query_params["category"]
    amount = request.GET.get("fixedLimit")

    if not (category and amount):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        amount = int(amount)
        category = int(category)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    avg_grade = request.data.get('avgGrade')
    sort_by = request.data.get('sortBy')
    sort_dir = request.data.get('sortDir')
    has_grades = request.data.get('hasGrades')

    categories_of_companies = CategoriesOfCompanies.objects.select_related('company').filter(category_id=category)
    company_ids = [category_of_company.company.id for category_of_company in categories_of_companies]
    results = companies_sorting_filtring(avg_grade, sort_by, sort_dir, has_grades)
    companies = results.filter(pk__in=company_ids)

    data = {'countAll': companies.count(),
            'countAllPages': (-(-companies.count() // amount))}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def refresh_token(request, *arg, **kwargs):
    """
    View that refresh jwt.
    :param request: Http request.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: access jwt with success status code or error code with details.
    """
    serializer = RefreshSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        data['access'] = serializer.data['access']
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=status_code)



@api_view(['POST'])
@authentication_classes([])
def auto_login(request, *args, **kwarg):
    """
    Automatic login provided by jwt token.
    :param request: Http request.
    :param args: Additional arguments passed to the view.
    :param kwarg: Additional keyword arguments passed to the view.
    :return: Response with jwt, user data and success status code or
    error status code with details.
    """
    serializer = RefreshSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        data = serializer.data
        status_code = status.HTTP_200_OK
    else:
        data = serializer.errors
        status_code = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=status_code)


@api_view(['POST'])
def search_companies(request, *arg, **kwargs):
    """
    Sorted and filtered list of companies containing search phrases within them.
    :param HttpRequest request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns a sorted and filtered list of companies containing the search term and HTTP code
    """
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
    """
    The function is used to reset the company's token
    :param HttpRequest request: HttpRequest object.
    :param arg: Additional arguments passed to the view.
    :param kwargs: Additional keyword arguments passed to the view.
    :return: Returns information about token change, new token, new safe words and HTTP code
    """
    serializer = ResetTokenSerializer()
    try:
        data = serializer.check_words(data=request.data)
        status_code = status.HTTP_200_OK
        return Response(data, status=status_code)
    except serializers.ValidationError as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
