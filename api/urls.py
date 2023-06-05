from django.urls import path


from . import views

urlpatterns = [
    path('', views.test),
    path('register', views.register),
    path('company', views.company),
    path('company/<int:pk>', views.company),
    path('opinion', views.opinion),
    path('category', views.categories),
    path('category/<int:pk>', views.categories),
    path('category/pageable', views.category_pageable),
    path('company/pageable', views.company_pageable),
    path('category/pageable/<int:amount>', views.category_pageable),
    path('company/<int:pk>/pageable/<int:amount>', views.company_pageable),
    path('search', views.search_companies),
    path('search/', views.search_companies, name="query"),

    path('login', views.login),
    path('company/login', views.login_company),
    path('token/refresh', views.refresh_token),
]