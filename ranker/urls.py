from django.urls import path

from . import views

urlpatterns = [
    path("search/<str:key>/",views.search,name ="search"),
    path('', views.index, name='index'),
]
