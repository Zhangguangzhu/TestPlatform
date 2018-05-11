# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.shortcuts import render
from . import models
# from django.core.urlresolvers import  reverse
from django.urls import reverse
from . import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required



# Create your views here.


def index(Request):
	return HttpResponse('hello')

def homepage(Request):
	title_obj = forms.VoteTitle()
	articles = models.Article.objects.all()
	return render(Request, 'blogapp/homepage.html', {'articles': articles,'title_obj':title_obj})


def article_page(request, article_prikey):
	article = models.Article.objects.get(pk=article_prikey)
	return render(request,'blogapp/article_page.html',{'article':article})

def test_page(Request, num):
	return HttpResponse('this is test page:%s' % (num))

def re_direct(request):
	return HttpResponseRedirect(reverse('blog', args=()))

def vote(request, article_prikey):
	article = models.Article.objects.get(pk=article_prikey)
	article.counter += 1
	article.save()
	return HttpResponseRedirect(reverse('blog:article_page', args=(article_prikey,)))
	# return HttpResponse("test")

def vote_all_result(request):
	errors_obj = " "
	if request.method == "POST":
		form_post = forms.VoteTitle(request.POST)
		if form_post.is_valid():
			title = form_post.cleaned_data['vote_title'] #is_valid 返回true后，post的值保存在cleaned_data 中以字典形式
			article = models.Article.objects.get(pk=title)
			article.counter += 1
			article.save()
		else:
			print 'error'
			errors_obj = form_post.errors
			# print form_post.errors["vote_title"]
			# print form_post.errors["vote_title"][0]
			# print type(form_post.errors["vote_title"])
	title_obj = forms.VoteTitle(
		initial={'vote_title':'标题1'} #列表默认值
	)
	articles = models.Article.objects.all()
	return render(request, 'blogapp/homepage.html', {'articles': articles,'title_obj':title_obj, 'errors_obj': errors_obj})

def upload_file(request):
	articles = models.Article.objects.all()
	if request.method == "POST":
		handle_upload_file(request.FILES['file'], str(request.FILES['file']))
		return HttpResponse('success')

def handle_upload_file(file, name):
	path = '/home/upload/'
	if not os.path.exists(path):
		os.mkdir(path)
	with open(os.path.join(path, name), 'wb+') as destination:
		for chunk in file.chunks():
			print len(chunk)
			destination.write(chunk)


def download_file(request, file):
	files = {}
	print file,'***********************'
	path = '/home/download/'
	file_path = os.path.join(path, file)
	if not os.path.exists(path):
		return HttpResponse('download failed:dir not exists')
	elif not os.path.exists(file_path):
		raise Http404('file not exists')
	if os.path.isdir(file_path):
		# files = [ file+'/'+filename for filename in os.listdir(file_path) ]
		for name in os.listdir(file_path):
			files[name] = file+'/'+name
		print files

		return render(request, 'blogapp/download_page.html', {'files':files})
	else:
		response = StreamingHttpResponse(readFile(file_path))
		response['Content-Type'] = 'application/octet-stream'
		# response['Content-Type'] = 'multipart/form-data'
		response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
		return response

def readFile(filename, chunk_size=512):
	with open(filename, 'rb') as f:
		while True:
			c = f.read(chunk_size)
			print len(c)
			if c:
				yield c
			else:
				break

def download_page(request):
	files = {}
	path = '/home/download/'
	for name in os.listdir(path):
		files[name] = name
	return render(request, 'blogapp/download_page.html', {'files':files})


def login(request):
	context = {}
	if request.method == 'POST':
		form = forms.UserInfo(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			passwd = form.cleaned_data['passwd']
			user = authenticate(username=username, password=passwd)
			if user:
				auth.login(request, user)
				request.session['username'] = username
				return HttpResponseRedirect(reverse('blog:homepage'))
			else:
				context = {'isLogin':False,'passwd':False}
				return render(request, 'blogapp/login.html', context)
	else:
		userinfo = forms.UserInfo()
		context = {'isLogin': False, 'passwd':True}
	return render(request, 'blogapp/login.html', {'userinfo':userinfo})


def register(request):
	context = {}
	if request.method == "POST":
		form = forms.UserInfo(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			passwd = form.cleaned_data['passwd']
			user = auth.authenticate(username=username, password=passwd)
			if user:
				context['userExit'] = True
				return render(request, 'blogapp/register.html', context)
			user = User.objects.create_user(username=username, password=passwd)
			user.save()
			request.session['username'] = username
			auth.login(request, user)
			return render(request, 'blogapp/homepage.html')
	else:
		# context = {'isLogin':False}
		userinfo = forms.UserInfo()
		return render(request, 'blogapp/register.html', {'userinfo':userinfo})