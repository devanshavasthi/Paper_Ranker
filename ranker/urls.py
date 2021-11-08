from django.urls import path

from . import views

urlpatterns = [
    path("search/<str:key>/",views.dbp,name ="search"),
    path('', views.index, name='index'),

    path('paper', views.paper, name='paper'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path("db",views.dbp),
    path("del",views.del_all)
]
