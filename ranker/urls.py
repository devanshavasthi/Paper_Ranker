from django.urls import path

from . import views

urlpatterns = [
    path("search/",views.SearchResultsView.as_view(),name ="search"),
    path('', views.indexView.as_view(), name='index'),
    path('paper', views.paper, name='paper'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('paperData', views.frequentView.as_view(), name='paperData'),
    path("pconf",views.printconf),
    path("del",views.del_all)
]
