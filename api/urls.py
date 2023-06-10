from django.urls import path


from . import views

urlpatterns = [
    path('', views.test),

    # auth
    path('login', views.login),
    path('register', views.register),
    path('company/login', views.login_company),
    path('token/reset', views.reset_token),
    path('token/refresh', views.refresh_token),
    path('login/auto', views.auto_login),

    # add company
    path('company', views.company),

    # get company by id
    path('company/<int:pk>', views.company),

    # add opinion by user
    path('opinion', views.opinion),

    # add response by company
    path('opinion/company', views.company_opinion),

    # get all opinions with pageable
    path('opinion/list/company/<int:company_id>', views.list_company_opinions),
    path('opinion/list/company/<int:company_id>/pageable', views.company_opinions_pageable),

    # get all categories
    path('category/pageable/<int:amount>', views.category_pageable),
    path('category', views.categories),
    path('category/all', views.categories_list),

    # get all company's by selected category
    path('category/company', views.companies_of_category, name="category"),
    path('category/company/pageable', views.company_category_pageable, name="category"),

    # get all company's by query
    path('search', views.search_companies, name="query"),
    path('company/pageable', views.company_pageable, name="query"),
]