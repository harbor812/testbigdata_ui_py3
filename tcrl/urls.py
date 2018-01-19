from django.conf.urls import url
from tcrl import views

urlpatterns=[
    url(r'^$',views.login,name='login'),
    url(r'^/login/$',views.login,name='login'),
    url(r'^/index/$',views.index,name='index'),
    url(r'^add/', views.add,name='add'),
]
