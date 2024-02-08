from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<slug>/', views.detail, name='detail'),
    path('post/<slug>/', views.post, name='post'),
    path('create_post', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('not_found/', views.not_found, name='not_found'),

]