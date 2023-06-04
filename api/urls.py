from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views

urlpatterns = [
    path('', views.test),
    path('register', views.register),
    path('company', views.company),
    path('company/<int:pk>', views.company),
    path('opinion', views.opinion),
    path('category', views.categories),
    path('category/<int:pk>', views.categories),
    path('category/pagable', views.category_pagable),
    path('category/pagable/<int:amount>', views.category_pagable),

    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]