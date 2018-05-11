# -*- coding: utf-8 -*-
from django.conf.urls import url
import views

urlpatterns = [
	 url(r'^article/(?P<article_prikey>[\w]*)$', views.article_page, name='article_page'),
	 url(r'^$', views.homepage, name='homepage'),
	 # url(r'^article/(?P<page>[\w]+-(?P<num>[\d]+))/$', views.test_page)
	url(r'^article/page-(?P<num>[\d]+)/$', views.test_page),
	url(r'^article/(?P<article_prikey>[\w]*)/vote/$', views.vote, name='vote'),
	url(r'article/vote/$', views.vote_all_result, name='vote_all'),
	url(r'^upload/$', views.upload_file, name='upload'),
	url(r'^download/(?P<file>[\w]+.*)/$', views.download_file, name='download_file'),
	url(r'^download/$', views.download_page, name='download'),
]