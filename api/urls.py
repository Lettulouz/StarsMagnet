from django.urls import path


from . import views

urlpatterns = [
    path('', views.test),
    path('register', views.register),
    path('company', views.company),
    path('company/<int:pk>', views.company),
    path('opinion', views.opinion),
    path('companyOpinion', views.company_opinion),
    path('category', views.categories),
    path('category/', views.companies_of_category, name="category"),
    path('category/pageable', views.category_pageable),
    path('company/pageable/<int:amount>', views.company_pageable, name="query"),
    path('category/pageable/<int:amount>', views.category_pageable),
    path('company/<int:pk>/pageable/<int:amount>', views.company_category_pageable),
    path('search/', views.search_companies, name="query"),
    path('reset/token', views.reset_token),

    path('login', views.login),
    path('company/login', views.login_company),
    path('token/refresh', views.refresh_token),
]