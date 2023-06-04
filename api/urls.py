from django.urls import path


from . import views

urlpatterns = [
    path('', views.test),
    path('register', views.register),
    path('company', views.company),
    path('category/<int:pk>', views.company),
    path('company/<int:pk>', views.company),
    path('opinion', views.opinion),
    path('categories', views.categories),


    path('login', views.login),
    path('token/refresh', views.refresh_token),
]