from django.urls import path, re_path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('support/', views.support, name='support'),
    path('up/', views.upload, name='upload'),
    path('login/', views.login_, name='login'),
    path('login/submit', views.login_submit, name='login_submit'),
    path('logout/', views.logout_, name='logout'),
    path('contato', views.contato, name='contato')
]
