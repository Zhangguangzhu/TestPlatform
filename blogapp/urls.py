# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	 url(r'^article/(?P<article_prikey>[\w]*)$', views.articlepage, name='article_page'),
	 url(r'^$', views.homepage, name='homepage'),
	 # url(r'^article/(?P<page>[\w]+-(?P<num>[\d]+))/$', views.test_page)
	url(r'^article/page-(?P<num>[\d]+)/$', views.test_page),
	# url(r'^article/(?P<article_prikey>[\w]*)/vote/$', views.vote, name='vote'),
	url(r'article/vote/$', views.vote_all_result, name='vote_all'),
	url(r'^upload/$', views.upload_file, name='upload'),
	url(r'^myarticle/$', views.myArticle, name='myArticle'),
	url(r'^myarticle/(?P<article_prikey>[\w]*)$', views.editArticle, name='editArticle'),
	# url(r'^download/(?P<file>[\w]+.*)$', views.download, name='download'),
]