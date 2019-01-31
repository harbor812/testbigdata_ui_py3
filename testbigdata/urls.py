"""testbigdata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from tcrl import views

urlpatterns = [
    # url(r'^test/$', views.GetMessageView.as_view()),
	url(r'^getcommentdetail', views.getcommentdetail, name='getcommentdetail'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^login', views.login, name='login'),
    url(r'^index', views.index, name='index'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^paomianfan_data', views.paomianfan_data, name='paomianfan_data'),
    url(r'^bigdata_data', views.paomianfan_data, name='paomianfan_data'),
    url(r'^other_data', views.paomianfan_data, name='paomianfan_data'),
    url(r'^bug_detail/(.*?)-(.*?)$', views.bug_detail, name='detail'),
    url(r'^bugname_detail/(.*?)-(.*?)-(.*?)$', views.bugname_detail, name='detail'),
    url(r'^bugmore_detail/(.*?)-(.*?)$', views.bugmore_detail, name='detail'),
    url(r'^jenkins_detail/(.*?)$', views.jenkins_detail, name='detail'),
    url(r'^jenkins1_detail/(.*?)$', views.jenkins1_detail, name='detail'),
    url(r'^jenkinsmore_detail/', views.jenkinsmore_detail, name='detail'),
    url(r'^changename_analyze/(.*?)$', views.changename_analyze),
    url(r'^day_search', views.day_search),
    url(r'^bug_search', views.bug_search),
    url(r'^jenkins_search', views.jenkins_search),
    url(r'^message', views.chat33),
    url(r'^echo_once1', views.echo_once1),
]