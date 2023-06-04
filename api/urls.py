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
    path('category/pageable', views.category_pagable),
    path('category/pageable/<int:amount>', views.category_pagable),

    path('login', views.login),
    path('company/login', views.login_company),
    path('token/refresh', views.refresh_token),
]